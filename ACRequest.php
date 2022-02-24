<?php

namespace common\requests;

use yii\httpclient\Exception;
use yii\httpclient\Request;
use yii\httpclient\Response;
use yii\web\BadRequestHttpException;

class ACRequest extends Request
{
    public const AC_URL = 'https://thealphacentauri.net';

    public function __construct($config = [])
    {
        parent::__construct($config);
        $this->setMethod('GET');

        $this->setUrl(self::AC_URL);
    }

    /**
     * @throws Exception
     * @throws BadRequestHttpException
     */
    public function send(string $id = ''): Response
    {
        $this->setUrl(sprintf('%s/%s', self::AC_URL, $id));
        $response = parent::send();
        if ($response->statusCode === '200' && $response->content !== null) {
            return $response;
        }
        throw new BadRequestHttpException($response->statusCode);
    }
}