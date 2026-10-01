<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use RuntimeException;

/**
 * NEARS-3979 — QA fixture: three module-1 default coupons for the group-tax / per-store coupon split.
 *
 *   Q3979P10   percent 10, no max_discount cap, min 0
 *   Q3979F25   fixed 25.00, min 20 (stores 12 + 14 at 20.00 each: store 12 takes 20.00, store 14 is truncated to 5.00)
 *   Q3979CAP8  percent 50, max_discount 8.00, min 0 (cap exhausted by one store)
 *
 * Idempotent (upsert by code). Local private copy only — never the shared multi_food_db.
 *
 *   DB_DATABASE=nears_qa_3979 php artisan db:seed --class=Nears3979GroupTaxCouponFixtureSeeder --force
 */
class Nears3979GroupTaxCouponFixtureSeeder extends Seeder
{
    public const ISOLATED_DB = 'nears_qa_3979';

    private const SHARED_DB = 'multi_food_db';

    private const LOCAL_HOSTS = ['127.0.0.1', 'localhost', '::1'];

    private const MODULE_ID = 1;

    public const COUPONS = [
        ['code' => 'Q3979P10', 'title' => 'Q3979 percent 10 no cap', 'discount_type' => 'percent', 'discount' => 10.00, 'min_purchase' => 0.00, 'max_discount' => 0.00],
        ['code' => 'Q3979F25', 'title' => 'Q3979 fixed 25 min 20', 'discount_type' => 'amount', 'discount' => 25.00, 'min_purchase' => 20.00, 'max_discount' => 0.00],
        ['code' => 'Q3979CAP8', 'title' => 'Q3979 percent 50 cap 8', 'discount_type' => 'percent', 'discount' => 50.00, 'min_purchase' => 0.00, 'max_discount' => 8.00],
    ];

    public function run(): void
    {
        $this->assertLocalPrivateCopy();

        DB::transaction(function () {
            foreach (self::COUPONS as $spec) {
                $existing = DB::table('coupons')->where('code', $spec['code'])->exists();
                $row = $spec + [
                    'start_date' => '2026-09-30',
                    'expire_date' => '2027-10-01',
                    'coupon_type' => 'default',
                    'limit' => null,
                    'status' => 1,
                    'data' => '""',
                    'module_id' => self::MODULE_ID,
                    'created_by' => 'admin',
                    'customer_id' => '["all"]',
                    'store_id' => null,
                    'updated_at' => now(),
                ];

                if ($existing) {
                    DB::table('coupons')->where('code', $spec['code'])->update($row);
                } else {
                    DB::table('coupons')->insert($row + ['total_uses' => 0, 'created_at' => now()]);
                }
            }
        });

        foreach (DB::table('coupons')->whereIn('code', array_column(self::COUPONS, 'code'))->orderBy('id')->get() as $c) {
            $this->command?->info("NEARS-3979: {$c->code} type={$c->discount_type} amount={$c->discount} min={$c->min_purchase} cap={$c->max_discount} module={$c->module_id}");
        }
    }

    private function assertLocalPrivateCopy(): void
    {
        $host = DB::connection()->getConfig('host');
        $connected = (string) DB::connection()->getDatabaseName();

        if (! in_array(is_string($host) ? $host : '', self::LOCAL_HOSTS, true)) {
            throw new RuntimeException('Nears3979GroupTaxCouponFixtureSeeder REFUSED: non-local database host.');
        }

        if ($connected !== self::ISOLATED_DB) {
            throw new RuntimeException(
                "Nears3979GroupTaxCouponFixtureSeeder REFUSED: connected database is \"{$connected}\"; only ".self::ISOLATED_DB.' is allowed (never '.self::SHARED_DB.').'
            );
        }
    }
}
