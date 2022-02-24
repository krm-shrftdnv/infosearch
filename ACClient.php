<?php

namespace common\requests;

use Yii;
use yii\base\InvalidConfigException;
use yii\httpclient\Client;

class ACClient extends Client
{
    /**
     * @return ACRequest
     * @throws InvalidConfigException
     */
    public function createRequest()
    {
        $config = $this->requestConfig;
        if (!isset($config['class'])) {
            $config['class'] = ACRequest::class;
        }
        $config['client'] = $this;
        return Yii::createObject($config);
    }
}