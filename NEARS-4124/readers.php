use App\Models\Order; use App\CentralLogics\OrderLogic; use App\Models\BusinessSetting;
echo "DB=".DB::select('select database() d')[0]->d."\n";
echo "wallet_status=".BusinessSetting::where('key','wallet_status')->value('value')." wallet_add_refund=".BusinessSetting::where('key','wallet_add_refund')->value('value')."\n";
foreach ([95001=>'UNTOUCHED twin of 94001 (digital_payment, unpaid)', 94001=>'94001 AFTER base courier PUT (digital_payment, paid)', 94002=>'94002 AFTER base PUT (stripe, paid)', 94005=>'94005 AFTER base PUT (wallet, paid)', 94006=>'94006 AFTER base PUT (offline_payment, paid)'] as $id=>$lbl) {
  $o=Order::withoutGlobalScopes()->find($id);
  $cancelPlan=OrderLogic::refundCreditPlan($o,false); $delPlan=OrderLogic::refundCreditPlan($o,true);
  echo "\n[$lbl] id=$id order_status={$o->order_status} method={$o->payment_method} payment_status={$o->payment_status} order_amount={$o->order_amount}\n";
  echo "  paymentEvidenceRefusal           => ".var_export(OrderLogic::paymentEvidenceRefusal($o),true)."\n";
  echo "  refundCreditPlan(cancel path)    => ".json_encode($cancelPlan)."   (refund_before_delivered :709-710 credit gate, in-tx admin digital_received decrement fires when payment_status=paid: ".($o->payment_status=='paid'?'YES -'.$o->order_amount:'no').")\n";
  echo "  refundCreditPlan(delivered/admin approve :620) => ".json_encode($delPlan)."\n";
  echo "  customer refund_request guard (Api/V1/OrderController:738: delivered && payment_status==paid) => ".var_export($o->order_status=='delivered' && $o->payment_status=='paid',true)."\n";
}
