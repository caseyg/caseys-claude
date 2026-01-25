[**rmapi-js**](../README.md)

***

# Interface: RemarkableApi

Defined in: [index.ts:369](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L369)

the api for accessing remarkable functions

There are roughly two types of functions.
- high-level api functions that provide simple access with a single round
  trip based on the web api
- low-level wrapped functions that take more round trips, but provide more
  control and may be faster since they can be cached.

Most of these functions validate the return values so that typescript is
accurate. However, sometimes those return values are more strict than the
"true" underlying types. If this happens, please [submit a an
issue](https://github.com/erikbrinkman/rmapi-js/issues). In the mean time,
you should be able to use the low level api to work around any restrictive
validation.

## Properties

<a id="raw"></a>

### raw

> **raw**: [`RawRemarkableApi`](RawRemarkableApi.md)

Defined in: [index.ts:371](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L371)

scoped access to the raw low-level api

## Methods

<a id="bulkdelete"></a>

### bulkDelete()

> **bulkDelete**(`hashes`, `refresh?`): `Promise`\<[`HashesEntry`](HashesEntry.md)\>

Defined in: [index.ts:685](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L685)

delete many entries

#### Parameters

##### hashes

readonly `string`[]

the hashes of the entries to delete

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashesEntry`](HashesEntry.md)\>

#### Example

```ts
await api.bulkDelete([file.hash]);
```

***

<a id="bulkmove"></a>

### bulkMove()

> **bulkMove**(`hashes`, `parent`, `refresh?`): `Promise`\<[`HashesEntry`](HashesEntry.md)\>

Defined in: [index.ts:669](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L669)

move many entries

#### Parameters

##### hashes

readonly `string`[]

an array of entry hashes to move

##### parent

`string`

the directory id to move the entries to, "" (root) and "trash" are special ids

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashesEntry`](HashesEntry.md)\>

#### Example

```ts
await api.bulkMove([file.hash], dir.id);
```

***

<a id="clearcache"></a>

### clearCache()

> **clearCache**(): `void`

Defined in: [index.ts:721](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L721)

completely delete the cache

If the cache is causing memory issues, you can clear it, but this will hurt
performance.

#### Returns

`void`

***

<a id="delete"></a>

### delete()

> **delete**(`hash`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:628](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L628)

delete an entry

#### Parameters

##### hash

`string`

the hash of the entry to delete

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.delete(file.hash);
```

***

<a id="dumpcache"></a>

### dumpCache()

> **dumpCache**(): `string`

Defined in: [index.ts:696](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L696)

get the current cache value as a string

You can use this to warm start a new instance of
[\`remarkable\`](../functions/remarkable.md) with any previously cached results.

#### Returns

`string`

***

<a id="getcontent"></a>

### getContent()

> **getContent**(`hash`): `Promise`\<[`Content`](../type-aliases/Content.md)\>

Defined in: [index.ts:415](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L415)

get the content metadata from an item hash

This takes the high level item hash, e.g. the hashes you get from
[\`listItems\`](#listitems) or [\`listIds\`](#listids).

#### Parameters

##### hash

`string`

the hash of the item to get content for

#### Returns

`Promise`\<[`Content`](../type-aliases/Content.md)\>

the content

#### Remarks

If this fails validation and you still want to get the content, you can use
the low-level api to get the raw text of the `.content` file in the
`RawEntry` for this hash.

***

<a id="getdocument"></a>

### getDocument()

> **getDocument**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [index.ts:469](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L469)

get the entire contents of a remarkable document

This gets every file of associated with a document, and puts them into a
zip archive.

#### Parameters

##### hash

`string`

the hash of the document to get the contents for (e.g. the
   hash received from `listItems`)

#### Returns

`Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

#### Remarks

This is an experimental feature, that works for downloading the raw version
of the document, but this format isn't understood enoguh to reput this on a
different remarkable, so that functionality is currently disabled.

***

<a id="getepub"></a>

### getEpub()

> **getEpub**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [index.ts:453](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L453)

get the epub associated with a document hash

This returns the raw input epub if a document was created from an epub.

#### Parameters

##### hash

`string`

the hash of the document to get the pdf for (e.g. the hash
    received from `listItems`)

#### Returns

`Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

the epub bytes

***

<a id="getmetadata"></a>

### getMetadata()

> **getMetadata**(`hash`): `Promise`\<[`Metadata`](Metadata.md)\>

Defined in: [index.ts:431](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L431)

get the metadata from an item hash

This takes the high level item hash, e.g. the hashes you get from
[\`listItems\`](#listitems) or [\`listIds\`](#listids).

#### Parameters

##### hash

`string`

the hash of the item to get metadata for

#### Returns

`Promise`\<[`Metadata`](Metadata.md)\>

the metadata

#### Remarks

If this fails validation and you still want to get the content, you can use
the low-level api to get the raw text of the `.metadata` file in the
`RawEntry` for this hash.

***

<a id="getpdf"></a>

### getPdf()

> **getPdf**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [index.ts:442](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L442)

get the pdf associated with a document hash

This returns the raw input pdf, not the rendered pdf with any markup.

#### Parameters

##### hash

`string`

the hash of the document to get the pdf for (e.g. the hash
    received from `listItems`)

#### Returns

`Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

the pdf bytes

***

<a id="listids"></a>

### listIds()

> **listIds**(`refresh?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)[]\>

Defined in: [index.ts:399](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L399)

similar to [\`listItems\`](#listitems) but backed by the low level api

#### Parameters

##### refresh?

`boolean`

if true, refresh the root hash before listing

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)[]\>

***

<a id="listitems"></a>

### listItems()

> **listItems**(`refresh?`): `Promise`\<[`Entry`](../type-aliases/Entry.md)[]\>

Defined in: [index.ts:392](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L392)

list all items

Items include both collections and documents. Documents that are in folders
will have their parent set to something other than "" or "trash", but
everything will be returned by this function.

#### Parameters

##### refresh?

`boolean`

if true, refresh the root hash before listing

#### Returns

`Promise`\<[`Entry`](../type-aliases/Entry.md)[]\>

a list of all items with some metadata

#### Example

```ts
await api.listItems();
```

#### Remarks

This is now backed by the low level api, and you may notice some
performance degradation if not taking advantage of the cache.

***

<a id="move"></a>

### move()

> **move**(`hash`, `parent`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:617](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L617)

move an entry

#### Parameters

##### hash

`string`

the hash of the file to move

##### parent

`string`

the id of the directory to move the entry to, "" (root) and "trash" are special parents

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.move(doc.hash, dir.id);
```

***

<a id="prunecache"></a>

### pruneCache()

> **pruneCache**(`refresh?`): `Promise`\<`void`\>

Defined in: [index.ts:713](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L713)

prune the cache so that it contains only reachable hashes

The cache is append only, so it can grow without bound, even as hashes
become unreachable. In the future, this may have better cache management to
track this in real time, but for now, you can call this method, to keep it
from growing continuously.

#### Parameters

##### refresh?

`boolean`

whether to refresh the root hash before pruning

#### Returns

`Promise`\<`void`\>

#### Remarks

This won't necessarily reduce the cache size. In order to see if
hashes are reachable we first have to search through all existing entry
lists.

***

<a id="putepub"></a>

### putEpub()

> **putEpub**(`visibleName`, `buffer`, `opts?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:507](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L507)

use the low-level api to add an epub document

Since this uses the low-level api, it provides more options than
[\`uploadEpub\`](#uploadepub), but is a little more finicky. Notably, it
may throw a [\`GenerationError\`](../classes/GenerationError.md) if the generation
doesn't match the current server generation, requiring you to retry until
it works.

#### Parameters

##### visibleName

`string`

the name to display on the reMarkable

##### buffer

`Uint8Array`

the raw epub

##### opts?

[`PutOptions`](PutOptions.md)

put options

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

the entry for the newly inserted document

#### Throws

GenerationError if the generation doesn't match the current server generation

***

<a id="putfolder"></a>

### putFolder()

> **putFolder**(`visibleName`, `opts?`, `refresh?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:514](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L514)

create a folder

#### Parameters

##### visibleName

`string`

##### opts?

[`FolderOptions`](FolderOptions.md)

##### refresh?

`boolean`

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

***

<a id="putpdf"></a>

### putPdf()

> **putPdf**(`visibleName`, `buffer`, `opts?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:486](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L486)

use the low-level api to add a pdf document

Since this uses the low-level api, it provides more options than
[\`uploadPdf\`](#uploadpdf), but is a little more finicky. Notably, it
may throw a [\`GenerationError\`](../classes/GenerationError.md) if the generation
doesn't match the current server generation, requiring you to retry until
it works.

#### Parameters

##### visibleName

`string`

the name to display on the reMarkable

##### buffer

`Uint8Array`

the raw pdf

##### opts?

[`PutOptions`](PutOptions.md)

put options

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

the entry for the newly inserted document

#### Throws

GenerationError if the generation doesn't match the current server generation

***

<a id="rename"></a>

### rename()

> **rename**(`hash`, `visibleName`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:640](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L640)

rename an entry

#### Parameters

##### hash

`string`

the hash of the entry to rename

##### visibleName

`string`

the new name to assign

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.rename(file.hash, "new name");
```

***

<a id="stared"></a>

### stared()

> **stared**(`hash`, `stared`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:656](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L656)

set if an entry is stared

#### Parameters

##### hash

`string`

the hash of the entry to rename

##### stared

`boolean`

whether the entry should be stared or not

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.stared(file.hash, true);
```

***

<a id="updatecollection"></a>

### updateCollection()

> **updateCollection**(`hash`, `content`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:583](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L583)

update content metadata for a collection

#### Parameters

##### hash

`string`

the hash of the file to update

##### content

`Partial`\<[`CollectionContent`](CollectionContent.md)\>

the fields of content to update

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.updateCollection(doc.hash, { textAlignment: "left" });
```

***

<a id="updatedocument"></a>

### updateDocument()

> **updateDocument**(`hash`, `content`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:566](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L566)

update content metadata for a document

#### Parameters

##### hash

`string`

the hash of the file to update

##### content

`Partial`\<[`DocumentContent`](DocumentContent.md)\>

the fields of content to update

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.updateDocument(doc.hash, { textAlignment: "left" });
```

***

<a id="updatetemplate"></a>

### updateTemplate()

> **updateTemplate**(`hash`, `content`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:600](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L600)

update content metadata for a template

#### Parameters

##### hash

`string`

the hash of the file to update

##### content

`Partial`\<[`TemplateContent`](TemplateContent.md)\>

the fields of content to update

##### refresh?

`boolean`

#### Returns

`Promise`\<[`HashEntry`](HashEntry.md)\>

#### Example

```ts
await api.updateTemplate(doc.hash, { textAlignment: "left" });
```

***

<a id="uploadepub"></a>

### uploadEpub()

> **uploadEpub**(`visibleName`, `buffer`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:534](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L534)

upload an epub

#### Parameters

##### visibleName

`string`

the name to show for the uploaded epub

##### buffer

`Uint8Array`

the epub contents

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

#### Example

```ts
await api.uploadEpub("My EPub", ...);
```

#### Remarks

this uses a simpler api that works even with schema version 4.

***

<a id="uploadfolder"></a>

### uploadFolder()

> **uploadFolder**(`visibleName`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:553](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L553)

create a folder using the simple api

#### Parameters

##### visibleName

`string`

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

***

<a id="uploadpdf"></a>

### uploadPdf()

> **uploadPdf**(`visibleName`, `buffer`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:550](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L550)

upload a pdf

#### Parameters

##### visibleName

`string`

the name to show for the uploaded epub

##### buffer

`Uint8Array`

the epub contents

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

#### Example

```ts
await api.uploadPdf("My PDF", ...);
```

#### Remarks

this uses a simpler api that works even with schema version 4.
