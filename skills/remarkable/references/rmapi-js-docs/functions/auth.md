[**rmapi-js**](../README.md)

***

# Function: auth()

> **auth**(`deviceToken`, `__namedParameters`): `Promise`\<`string`\>

Defined in: [index.ts:1527](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1527)

Exchange a device token for a session token.

## Parameters

### deviceToken

`string`

the device token proving this api instance is
   registered. Create one with [register](register.md).

### \_\_namedParameters

[`AuthOptions`](../interfaces/AuthOptions.md) = `{}`

## Returns

`Promise`\<`string`\>

the session token returned by the reMarkable service
