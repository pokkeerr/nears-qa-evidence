<?php
// QA-only request recorder for NEARS-3977 baseline. Logs cart endpoints only
// (method, path, query, moduleId/zoneId headers, body, status). No auth headers.
$__path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (strpos($__path, '/api/v1/customer/cart') === 0) {
    $__rec = [
        'ts' => sprintf('%.3f', microtime(true)),
        'iso' => date('H:i:s'),
        'method' => $_SERVER['REQUEST_METHOD'],
        'path' => $__path,
        'query' => $_SERVER['QUERY_STRING'] ?? '',
        'moduleId' => $_SERVER['HTTP_MODULEID'] ?? null,
        'zoneId' => $_SERVER['HTTP_ZONEID'] ?? null,
        'body' => file_get_contents('php://input'),
    ];
    register_shutdown_function(function () use ($__rec) {
        $__rec['status'] = http_response_code();
        file_put_contents('/Users/Apple/.nears/qa/NEARS-3977/baseline/requests.jsonl',
            json_encode($__rec, JSON_UNESCAPED_SLASHES) . "\n", FILE_APPEND | LOCK_EX);
    });
}
return require '/Users/Apple/Projects/nears/Admin/server.php';
