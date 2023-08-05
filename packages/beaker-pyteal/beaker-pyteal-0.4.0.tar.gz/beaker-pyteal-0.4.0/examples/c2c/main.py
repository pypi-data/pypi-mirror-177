from pyteal import (
    Approve,
    OnComplete,
    abi,
    TealType,
    TxnType,
    Seq,
    Assert,
    Len,
    InnerTxnBuilder,
    TxnField,
    Int,
    InnerTxn,
    ScratchVar,
    Bytes,
    Log,
)
import beaker as bkr
from beaker.application import get_method_signature

algod_client = bkr.sandbox.get_algod_client()


class C2CSub(bkr.Application):
    """Sub application who's only purpose is to opt into then close out of an asset"""

    rasv = bkr.ReservedApplicationStateValue(TealType.bytes, 1)
    asv = bkr.ApplicationStateValue(TealType.bytes, default=Bytes("asv"))

    racsv = bkr.ReservedAccountStateValue(TealType.bytes, 1)
    acsv = bkr.AccountStateValue(TealType.bytes, default=Bytes("acsv"))

    @bkr.create
    def create(self):
        return Seq(self.initialize_application_state(), Approve())

    @bkr.opt_in
    def opt_in(self):
        return Seq(self.initialize_account_state(), Approve())

    @bkr.external
    def opt_in_to_asset(self, asset: abi.Asset):
        return InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: asset.asset_id(),
                TxnField.asset_receiver: self.address,
                TxnField.fee: Int(0),
                TxnField.asset_amount: Int(0),
            }
        )

    @bkr.external
    def return_asset(self, asset: abi.Asset, addr: abi.Account):
        return InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetTransfer,
                TxnField.xfer_asset: asset.asset_id(),
                TxnField.asset_receiver: addr.address(),
                TxnField.fee: Int(0),
                TxnField.asset_amount: Int(0),
                TxnField.asset_close_to: addr.address(),
            }
        )


class C2CMain(bkr.Application):
    """Main application that handles creation of the sub app and asset and calls it"""

    # Create sub app to be precompiled before allowing TEAL generation
    sub_app: bkr.AppPrecompile = bkr.AppPrecompile(C2CSub())

    @bkr.external
    def create_sub(self, *, output: abi.Uint64):
        return Seq(
            InnerTxnBuilder.Execute(self.sub_app.get_create_config()),
            # return the app id of the newly created app
            output.set(InnerTxn.created_application_id()),
            # Try to read the global state
            sv := C2CSub.asv.get_external(output.get()),
            Log(sv.value()),
            # Opt in to the new app for funsies
            InnerTxnBuilder.Execute(
                {
                    TxnField.type_enum: TxnType.ApplicationCall,
                    TxnField.application_id: output.get(),
                    TxnField.on_completion: OnComplete.OptIn,
                }
            ),
            # Try to read the local state
            sv := C2CSub.acsv[self.address].get_external(output.get()),
            Log(sv.value()),
        )

    @bkr.internal(TealType.uint64)
    def create_asset(self, name):
        return Seq(
            InnerTxnBuilder.Execute(
                {
                    TxnField.type_enum: TxnType.AssetConfig,
                    TxnField.config_asset_name: name,
                    TxnField.config_asset_total: Int(10),
                    TxnField.config_asset_manager: self.address,
                }
            ),
            # return the newly created asset id
            InnerTxn.created_asset_id(),
        )

    @bkr.internal(TealType.none)
    def trigger_opt_in_and_xfer(self, app_id, app_addr, asset_id):
        # Call the sub app to make it opt in and xfer it some tokens
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.MethodCall(
                app_id=app_id,
                method_signature=get_method_signature(C2CSub.opt_in_to_asset),
                args=[asset_id],
            ),
            InnerTxnBuilder.Next(),
            InnerTxnBuilder.SetFields(
                {
                    TxnField.type_enum: TxnType.AssetTransfer,
                    TxnField.xfer_asset: asset_id,
                    TxnField.asset_amount: Int(1),
                    TxnField.asset_receiver: app_addr,
                }
            ),
            InnerTxnBuilder.Submit(),
        )

    @bkr.internal(TealType.none)
    def trigger_return(self, app_id, asset_id):
        # Create the group txn to ask sub app to opt in and send sub app 1 token
        # Tell the sub app to send me back the stuff i sent it
        return Seq(
            InnerTxnBuilder.Begin(),
            InnerTxnBuilder.MethodCall(
                app_id=app_id,
                method_signature=get_method_signature(C2CSub.return_asset),
                args=[asset_id, self.address],
            ),
            InnerTxnBuilder.Submit(),
        )

    @bkr.external
    def create_asset_and_send(
        self, name: abi.String, sub_app_ref: abi.Application, *, output: abi.Uint64
    ):
        return Seq(
            Assert(Len(name.get())),
            # Create the asset
            (asset_id := ScratchVar()).store(self.create_asset(name.get())),
            # Get the sub app addr
            (sub_app_addr := sub_app_ref.params().address()),
            # Ask sub app to opt in, and send asset in the same group
            self.trigger_opt_in_and_xfer(
                sub_app_ref.application_id(), sub_app_addr.value(), asset_id.load()
            ),
            # Get the asset back
            self.trigger_return(sub_app_ref.application_id(), asset_id.load()),
            # Return the asset id
            output.set(asset_id.load()),
        )

    @bkr.external
    def delete_asset(self, asset: abi.Asset):
        return InnerTxnBuilder.Execute(
            {
                TxnField.type_enum: TxnType.AssetConfig,
                TxnField.config_asset: asset.asset_id(),
            }
        )


def demo():

    accts = bkr.sandbox.get_accounts()
    acct = accts.pop()
    algod_client = bkr.sandbox.get_algod_client()

    # Create main app and fund it
    app_client = bkr.client.ApplicationClient(
        algod_client, C2CMain(), signer=acct.signer
    )
    main_app_id, _, _ = app_client.create()

    print(f"Created main app: {main_app_id}")
    app_client.fund(1 * bkr.consts.algo)

    # Call the main app to create the sub app
    result = app_client.call(C2CMain.create_sub)
    print(result.tx_info)
    sub_app_id = result.return_value
    print(f"Created sub app: {sub_app_id}")

    # Call main app method to:
    #   create the asset
    #   call the sub app optin method
    #   send asset to sub app
    #   call the sub app return asset method
    sp = app_client.client.suggested_params()
    sp.flat_fee = True
    sp.fee = 1 * bkr.consts.algo
    result = app_client.call(
        C2CMain.create_asset_and_send,
        name="dope asset",
        sub_app_ref=sub_app_id,
        suggested_params=sp,
    )
    created_asset = result.return_value
    print(f"Created asset id: {created_asset}")

    result = app_client.call(
        C2CMain.delete_asset,
        asset=created_asset,
    )
    print(f"Deleted asset in tx: {result.tx_id}")


if __name__ == "__main__":
    demo()
