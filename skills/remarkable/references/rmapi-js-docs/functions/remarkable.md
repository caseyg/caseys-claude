[**rmapi-js**](../README.md)

***

# Function: remarkable()

> **remarkable**(`deviceToken`, `options`): `Promise`\<[`RemarkableApi`](../interfaces/RemarkableApi.md)\>

Defined in: [index.ts:1585](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1585)

create an instance of the api

This gets a temporary authentication token with the device token and then
constructs the api instance.

## Parameters

### deviceToken

`string`

the device token proving this api instance is
   registered. Create one with [register](register.md).

### options

[`RemarkableOptions`](../interfaces/RemarkableOptions.md) = `{}`

## Returns

`Promise`\<[`RemarkableApi`](../interfaces/RemarkableApi.md)\>

an api instance
