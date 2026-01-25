[**rmapi-js**](../README.md)

***

# Function: register()

> **register**(`code`, `__namedParameters`): `Promise`\<`string`\>

Defined in: [index.ts:259](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L259)

register a device and get the token needed to access the api

Have users go to `https://my.remarkable.com/device/browser/connect` and pass
the resulting code into this function to get a device token. Persist that
token to use the api.

## Parameters

### code

`string`

the eight letter code a user got from `https://my.remarkable.com/device/browser/connect`.

### \_\_namedParameters

[`RegisterOptions`](../interfaces/RegisterOptions.md) = `{}`

## Returns

`Promise`\<`string`\>

the device token necessary for creating an api instace. These never expire so persist as long as necessary.
