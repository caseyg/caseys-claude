[**rmapi-js**](../README.md)

***

# Interface: RemarkableSessionOptions

Defined in: [index.ts:1468](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1468)

options for constructing an api instance from a session token

## Extended by

- [`RemarkableOptions`](RemarkableOptions.md)

## Properties

<a id="cache"></a>

### cache?

> `optional` **cache**: `string`

Defined in: [index.ts:1496](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1496)

an initial cache value

Generated from calling [\`dumpCache\`](RemarkableApi.md#dumpcache) on a previous
instance.

***

<a id="maxcachesize"></a>

### maxCacheSize?

> `optional` **maxCacheSize**: `number`

Defined in: [index.ts:1507](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1507)

the maximum size of the cache in terms of total string length

By the JavaScript specification there are two bytes per character, but the
total memory usage of the cache will also be larger than just the size of
the data stored.

#### Default Value

```ts
Infinity
```

***

<a id="rawhost"></a>

### rawHost?

> `optional` **rawHost**: `string`

Defined in: [index.ts:1488](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1488)

the url for making requests using the low-level api

#### Default Value

```ts
"https://eu.tectonic.remarkable.com"
```

***

<a id="synchost"></a>

### syncHost?

> `optional` **syncHost**: `string`

Defined in: [index.ts:1474](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1474)

the url for making synchronization requests

#### Default Value

```ts
"https://web.eu.tectonic.remarkable.com"
```

***

<a id="uploadhost"></a>

### uploadHost?

> `optional` **uploadHost**: `string`

Defined in: [index.ts:1481](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L1481)

the base url for making upload requests

#### Default Value

```ts
"https://internal.cloud.remarkable.com"
```
