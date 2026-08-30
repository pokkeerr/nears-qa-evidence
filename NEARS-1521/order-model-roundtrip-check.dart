import 'package:sixam_mart/features/order/domain/models/order_model.dart';

void main() {
  // Case 1: field present with a value.
  final present = OrderModel.fromJson({'id': 1, 'estimated_delivery_at': '2026-08-27 08:40:00'});
  print('present: ${present.estimatedDeliveryAt}');
  assert(present.estimatedDeliveryAt == '2026-08-27 08:40:00');

  // Case 2: field present but explicitly null.
  final nullVal = OrderModel.fromJson({'id': 2, 'estimated_delivery_at': null});
  print('nullVal: ${nullVal.estimatedDeliveryAt}');
  assert(nullVal.estimatedDeliveryAt == null);

  // Case 3: field absent from JSON entirely.
  final absent = OrderModel.fromJson({'id': 3});
  print('absent: ${absent.estimatedDeliveryAt}');
  assert(absent.estimatedDeliveryAt == null);

  // toJson round trip for the present case.
  final json = present.toJson();
  print('toJson estimated_delivery_at: ${json['estimated_delivery_at']}');
  assert(json['estimated_delivery_at'] == '2026-08-27 08:40:00');

  // toJson round trip for the null case (key exists, value null -- must not throw).
  final jsonNull = nullVal.toJson();
  print('toJson (null case) contains key: ${jsonNull.containsKey('estimated_delivery_at')}, value: ${jsonNull['estimated_delivery_at']}');

  print('ALL ASSERTIONS PASSED');
}
