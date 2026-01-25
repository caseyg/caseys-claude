[**rmapi-js**](../README.md)

***

# Interface: RegisterOptions

Defined in: [index.ts:226](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L226)

options for registering with the api

## Properties

<a id="authhost"></a>

### authHost?

> `optional` **authHost**: `string`

Defined in: [index.ts:246](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L246)

The host to use for authorization requests

***

<a id="devicedesc"></a>

### deviceDesc?

> `optional` **deviceDesc**: `"desktop-windows"` \| `"desktop-macos"` \| `"desktop-linux"` \| `"mobile-android"` \| `"mobile-ios"` \| `"browser-chrome"` \| `"remarkable"`

Defined in: [index.ts:232](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L232)

the device description to use

Using an improper one will results in the registration being rejected.

***

<a id="uuid"></a>

### uuid?

> `optional` **uuid**: `string`

Defined in: [index.ts:244](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L244)

the unique id of this device

If omitted it will be randomly generated
