[**rmapi-js**](../README.md)

***

# Interface: RawRemarkableApi

Defined in: [raw.ts:756](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L756)

access to the low-level reMarkable api

This class gives more granualar access to the reMarkable cloud, but is more
dangerous.

## Overview

reMarkable uses an immutable file system, where each file is referenced by
the 32 byte sha256 hash of its contents. Each file also has an id used to
keep track of updates, so to "update" a file, you upload a new file, and
change the hash associated with it's id.

Each "item" (a document or a collection) is actually a list of files.
The whole reMarkable state is then a list of these lists. Finally, the hash
of that list is called the rootHash. To update anything, you have to update
the root hash to point to a new list of updated items.

This can be dangerous, as corrupting the root hash can destroy all of your
files. It is therefore highly recommended to save your current root hash
([\`getRootHash\`](#getroothash)) before using this api to attempt file
writes, so you can recover a previous "snapshot" should anything go wrong.

## Items

Each item is a collection of individual files. Using
[\`getEntries\`](#getentries) on the root hash will give you a list
entries that correspond to items. Using `getEntries` on any of those items
will get you the files that make up that item.

The documented files are:
- `<docid>.pdf` - a raw pdf document
- `<docid>.epub` - a raw epub document
- `<docid>.content` - a json file roughly describing document properties (see [\`DocumentContent\`](DocumentContent.md))
- `<docid>.metadata` - metadata about the document (see [\`Metadata\`](Metadata.md))
- `<docid>.pagedata` - a text file where each line is the template of that page
- `<docid>/<pageid>.rm` - [speculative] raw remarkable vectors, text, etc
- `<docid>/<pageid>-metadata.json` - [speculative] metadata about the individual page
- `<docid>.highlights/<pageid>.json` - [speculative] highlights on the page

Some items will have both a `.pdf` and `.epub` file, likely due to preparing
for export. Collections only have `.content` and `.metadata` files, with
`.content` only containing tags.

## Caching

Since everything is tied to the hash of it's contents, we can agressively
cache results. We assume that text contents are "small" and so fully cache
them, where as binary files we treat as large and only store that we know
they exist to prevent future writes.

By default, this only persists as long as the api instance is alive. However,
for performance reasons, you should call [\`dumpCache\`](#dumpcache) to
persist the cache between sessions.

## Remarks

Generally all hashes are 64 character hex strings, and all ids are uuid4.

## Methods

<a id="clearcache"></a>

### clearCache()

> **clearCache**(): `void`

Defined in: [raw.ts:920](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L920)

completely clear the cache

#### Returns

`void`

***

<a id="dumpcache"></a>

### dumpCache()

> **dumpCache**(): `string`

Defined in: [raw.ts:917](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L917)

dump the current cache to a string to preserve between session

#### Returns

`string`

a serialized version of the cache to pass to a new api instance

***

<a id="getcontent"></a>

### getContent()

> **getContent**(`hash`): `Promise`\<[`Content`](../type-aliases/Content.md)\>

Defined in: [raw.ts:806](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L806)

get the parsed and validated `Content` of a content hash

Use [\`getText\`](#gettext) combined with `JSON.parse` to bypass
validation

#### Parameters

##### hash

`string`

the hash to get Content for

#### Returns

`Promise`\<[`Content`](../type-aliases/Content.md)\>

the content

***

<a id="getentries"></a>

### getEntries()

> **getEntries**(`hash`): `Promise`\<[`Entries`](Entries.md)\>

Defined in: [raw.ts:795](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L795)

get the entries associated with a list hash

A list hash is the root hash, or any hash with the type 80000000. NOTE
these are hashed differently than files.

#### Parameters

##### hash

`string`

the hash to get entries for

#### Returns

`Promise`\<[`Entries`](Entries.md)\>

the entries

***

<a id="gethash"></a>

### getHash()

> **getHash**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [raw.ts:773](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L773)

get the raw binary data associated with a hash

#### Parameters

##### hash

`string`

the hash to get the data for

#### Returns

`Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

the data

***

<a id="getmetadata"></a>

### getMetadata()

> **getMetadata**(`hash`): `Promise`\<[`Metadata`](Metadata.md)\>

Defined in: [raw.ts:817](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L817)

get the parsed and validated `Metadata` of a metadata hash

Use [\`getText\`](#gettext) combined with `JSON.parse` to bypass
validation

#### Parameters

##### hash

`string`

the hash to get Metadata for

#### Returns

`Promise`\<[`Metadata`](Metadata.md)\>

the metadata

***

<a id="getroothash"></a>

### getRootHash()

> **getRootHash**(): `Promise`\<\[`string`, `number`, [`SchemaVersion`](../type-aliases/SchemaVersion.md)\]\>

Defined in: [raw.ts:765](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L765)

gets the root hash and the current generation

When calling `putRootHash`, you should pass the generation you got from
this call. That way you tell reMarkable you're updating the previous state.

#### Returns

`Promise`\<\[`string`, `number`, [`SchemaVersion`](../type-aliases/SchemaVersion.md)\]\>

the root hash and the current generation

***

<a id="gettext"></a>

### getText()

> **getText**(`hash`): `Promise`\<`string`\>

Defined in: [raw.ts:784](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L784)

get raw text data associated with a hash

We assume text data are small, and so cache the entire text. If you want to
avoid this, use [\`getHash\`](#gethash) combined with a TextDecoder.

#### Parameters

##### hash

`string`

the hash to get text for

#### Returns

`Promise`\<`string`\>

the text

***

<a id="putcontent"></a>

### putContent()

> **putContent**(`id`, `content`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:864](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L864)

the same as [\`putText\`](#puttext) but with extra validation for Content

#### Parameters

##### id

`string`

##### content

[`Content`](../type-aliases/Content.md)

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

***

<a id="putentries"></a>

### putEntries()

> **putEntries**(`id`, `entries`, `schemaVersion`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:887](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L887)

put a set of entries to make an entry list file

To fully upload an item:
1. upload all the constituent files and metadata
2. call this with all of the entries
3. append this entry to the root entry and call this again to update this root list
4. put the new root hash

#### Parameters

##### id

`string`

the id of the list to upload - this should be the item id if
  uploading an item list, or "root" if uploading a new root list.

##### entries

[`RawEntry`](RawEntry.md)[]

the entries to upload

##### schemaVersion

[`SchemaVersion`](../type-aliases/SchemaVersion.md)

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

the new list entry and a promise to finish the upload

***

<a id="putfile"></a>

### putFile()

> **putFile**(`id`, `bytes`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:858](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L858)

put a raw onto the server

This returns the new expeced entry of the file you uploaded, and a promise
to finish the upload successful. By splitting these two operations you can
start using the uploaded entry while file finishes uploading.

NOTE: This won't update the state of the reMarkable until this entry is
incorporated into the root hash.

#### Parameters

##### id

`string`

the id of the file to upload

##### bytes

`Uint8Array`

the bytes to upload

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

the new entry and a promise to finish the upload

***

<a id="putmetadata"></a>

### putMetadata()

> **putMetadata**(`id`, `metadata`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:867](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L867)

the same as [\`putText\`](#puttext) but with extra validation for Metadata

#### Parameters

##### id

`string`

##### metadata

[`Metadata`](Metadata.md)

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

***

<a id="putroothash"></a>

### putRootHash()

> **putRootHash**(`hash`, `generation`, `broadcast?`): `Promise`\<\[`string`, `number`\]\>

Defined in: [raw.ts:838](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L838)

update the current root hash

This will fail if generation doesn't match the current server generation.
This ensures that you are updating what you expect. IF you get a
[\`GenerationError\`](../classes/GenerationError.md), that indicates that the server
was updated after you last got the generation. You should call
[\`getRootHash\`](#getroothash) and then recompute the changes you want
from the new root hash. If you ignore the update hash value and just call
`putRootHash` again, you will overwrite the changes made by the other
update.

#### Parameters

##### hash

`string`

the new root hash

##### generation

`number`

the generation of the current root hash

##### broadcast?

`boolean`

[unknown] an option in the request

#### Returns

`Promise`\<\[`string`, `number`\]\>

the new root hash and the new generation

#### Throws

GenerationError if the generation doesn't match the current server generation

***

<a id="puttext"></a>

### putText()

> **putText**(`id`, `content`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:861](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L861)

the same as [\`putFile\`](#putfile) but with caching for text

#### Parameters

##### id

`string`

##### content

`string`

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

***

<a id="uploadfile"></a>

### uploadFile()

> **uploadFile**(`visibleName`, `bytes`, `mime`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [raw.ts:906](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L906)

upload a file to the reMarkable cloud using the simple api

This api is the same as used by the native reMarkable extension and works
even if the backend schema version is version 4. Setting mime to "folder"
allows folder creation.

#### Parameters

##### visibleName

`string`

the name of the file as it should appear on the reMarkable

##### bytes

`Uint8Array`

the bytes of the file to upload

##### mime

[`UploadMimeType`](../type-aliases/UploadMimeType.md)

the mime type of the file to upload

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

a simple entry with the id and hash of the uploaded file
