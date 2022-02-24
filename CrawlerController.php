<?php

namespace console\controllers;

use common\requests\ACClient;
use common\requests\ACRequest;
use Yii;
use yii\base\InvalidConfigException;
use yii\console\Controller;
use yii\helpers\FileHelper;
use yii\httpclient\Exception;
use yii\web\BadRequestHttpException;

class CrawlerController extends Controller
{
    /**
     * @throws Exception
     * @throws InvalidConfigException
     */
    public function actionParse()
    {
        $beginId = 90935;
        $results = [];
        $index = '';
        $client = new ACClient();
        $id = $beginId;
        $request = $client->createRequest();
        $storagePath = Yii::getAlias('@common') . "\storage\\";
        while (count($results) < 70) {
            try {
                $response = $request->send((string)$id);
                $index.= sprintf("%d - %s/%d\n", $id, ACRequest::AC_URL, $id);
                $results[$id] = $response->content;
                $filename = sprintf('%s%s.html', $storagePath, (string)$id);
                file_put_contents($filename, $response->content);
            } catch (BadRequestHttpException $e) {
                echo $e->getMessage()."\n";
            }
            echo $id."\n";
            $id++;
            sleep(2);
        }
        echo $index;
    }

    public function actionIndex()
    {
        $storagePath = Yii::getAlias('@common') . "\storage\\";
        $files= FileHelper::findFiles($storagePath);
        $content = '';
        foreach ($files as $file) {
            $id = explode('.', array_reverse(explode('\\', $file))[0])[0];
            $content .= sprintf("%s - %s/%s\n", $id, ACRequest::AC_URL, $id);
        }
        file_put_contents($storagePath.'index.txt', $content);
    }
}