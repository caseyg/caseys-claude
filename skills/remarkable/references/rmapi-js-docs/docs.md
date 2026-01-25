

---

<!-- source: classes/GenerationError.md -->

[**rmapi-js**](../README.md)

***

# Class: GenerationError

Defined in: [index.ts:201](src/index.ts#L201)

An error that gets thrown when the backend while trying to update

IF you encounter this error, you likely just need to try th request again. If
you're trying to do several high-level `put` operations simultaneously,
you'll likely encounter this error. You should either try to do them
serially, or call the low level api directly to do one generation update.

## See

[\`RawRemarkableApi\`](../interfaces/RawRemarkableApi.md)

## Extends

- `Error`

## Constructors

### Constructor

> **new GenerationError**(): `GenerationError`

Defined in: [index.ts:202](src/index.ts#L202)

#### Returns

`GenerationError`

#### Overrides

`Error.constructor`


---

<!-- source: classes/HashNotFoundError.md -->

[**rmapi-js**](../README.md)

***

# Class: HashNotFoundError

Defined in: [error.ts:16](src/error.ts#L16)

an error that results while supplying a hash not found in the entries of the root hash

## Extends

- `Error`

## Constructors

### Constructor

> **new HashNotFoundError**(`hash`): `HashNotFoundError`

Defined in: [error.ts:20](src/error.ts#L20)

#### Parameters

##### hash

`string`

#### Returns

`HashNotFoundError`

#### Overrides

`Error.constructor`

## Properties

### hash

> `readonly` **hash**: `string`

Defined in: [error.ts:18](src/error.ts#L18)

the hash that couldn't be found


---

<!-- source: classes/ResponseError.md -->

[**rmapi-js**](../README.md)

***

# Class: ResponseError

Defined in: [index.ts:208](src/index.ts#L208)

an error that results from a failed request

## Extends

- `Error`

## Constructors

### Constructor

> **new ResponseError**(`status`, `statusText`, `message`): `ResponseError`

Defined in: [index.ts:214](src/index.ts#L214)

#### Parameters

##### status

`number`

##### statusText

`string`

##### message

`string`

#### Returns

`ResponseError`

#### Overrides

`Error.constructor`

## Properties

### status

> `readonly` **status**: `number`

Defined in: [index.ts:210](src/index.ts#L210)

the response status number

***

### statusText

> `readonly` **statusText**: `string`

Defined in: [index.ts:212](src/index.ts#L212)

the response status text


---

<!-- source: classes/ValidationError.md -->

[**rmapi-js**](../README.md)

***

# Class: ValidationError

Defined in: [error.ts:2](src/error.ts#L2)

an error that results from a failed request

## Extends

- `Error`

## Constructors

### Constructor

> **new ValidationError**(`field`, `regex`, `message`): `ValidationError`

Defined in: [error.ts:8](src/error.ts#L8)

#### Parameters

##### field

`string`

##### regex

`RegExp`

##### message

`string`

#### Returns

`ValidationError`

#### Overrides

`Error.constructor`

## Properties

### field

> `readonly` **field**: `string`

Defined in: [error.ts:4](src/error.ts#L4)

the response status number

***

### regex

> `readonly` **regex**: `RegExp`

Defined in: [error.ts:6](src/error.ts#L6)

the response status text


---

<!-- source: functions/auth.md -->

[**rmapi-js**](../README.md)

***

# Function: auth()

> **auth**(`deviceToken`, `__namedParameters`): `Promise`\<`string`\>

Defined in: [index.ts:1527](src/index.ts#L1527)

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


---

<!-- source: functions/register.md -->

[**rmapi-js**](../README.md)

***

# Function: register()

> **register**(`code`, `__namedParameters`): `Promise`\<`string`\>

Defined in: [index.ts:259](src/index.ts#L259)

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


---

<!-- source: functions/remarkable.md -->

[**rmapi-js**](../README.md)

***

# Function: remarkable()

> **remarkable**(`deviceToken`, `options`): `Promise`\<[`RemarkableApi`](../interfaces/RemarkableApi.md)\>

Defined in: [index.ts:1585](src/index.ts#L1585)

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


---

<!-- source: functions/session.md -->

[**rmapi-js**](../README.md)

***

# Function: session()

> **session**(`sessionToken`, `__namedParameters`): [`RemarkableApi`](../interfaces/RemarkableApi.md)

Defined in: [index.ts:1552](src/index.ts#L1552)

Create an API instance from an existing session token.

If requests start failing, simply recreate the api instance with a freshly
fetched session token.

## Parameters

### sessionToken

`string`

the session token used for authorization

### \_\_namedParameters

[`RemarkableSessionOptions`](../interfaces/RemarkableSessionOptions.md) = `{}`

## Returns

[`RemarkableApi`](../interfaces/RemarkableApi.md)

an api instance


---

<!-- source: interfaces/AuthOptions.md -->

[**rmapi-js**](../README.md)

***

# Interface: AuthOptions

Defined in: [index.ts:1458](src/index.ts#L1458)

configuration for exchanging a device token

## Extended by

- [`RemarkableOptions`](RemarkableOptions.md)

## Properties

### authHost?

> `optional` **authHost**: `string`

Defined in: [index.ts:1464](src/index.ts#L1464)

the url for making authorization requests

#### Default Value

```ts
"https://webapp-prod.cloud.remarkable.engineering"
```


---

<!-- source: interfaces/CollectionContent.md -->

[**rmapi-js**](../README.md)

***

# Interface: CollectionContent

Defined in: [raw.ts:319](src/raw.ts#L319)

the content metadata for collections (folders)

## Properties

### fileType?

> `optional` **fileType**: `undefined`

Defined in: [raw.ts:324](src/raw.ts#L324)

collections don't have a file type

***

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [raw.ts:321](src/raw.ts#L321)

the tags for the collection


---

<!-- source: interfaces/CollectionEntry.md -->

[**rmapi-js**](../README.md)

***

# Interface: CollectionEntry

Defined in: [index.ts:144](src/index.ts#L144)

a folder, referred to in the api as a collection

## Extends

- [`EntryCommon`](EntryCommon.md)

## Properties

### hash

> **hash**: `string`

Defined in: [index.ts:125](src/index.ts#L125)

the current hash of the state of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`hash`](EntryCommon.md#hash)

***

### id

> **id**: `string`

Defined in: [index.ts:123](src/index.ts#L123)

the document id, a uuid4

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`id`](EntryCommon.md#id)

***

### lastModified

> **lastModified**: `string`

Defined in: [index.ts:129](src/index.ts#L129)

the last modified timestamp

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`lastModified`](EntryCommon.md#lastmodified)

***

### pinned

> **pinned**: `boolean`

Defined in: [index.ts:131](src/index.ts#L131)

true if the entry is starred in most ui elements

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`pinned`](EntryCommon.md#pinned)

***

### type

> **type**: `"CollectionType"`

Defined in: [index.ts:146](src/index.ts#L146)

the key for this as a collection

***

### visibleName

> **visibleName**: `string`

Defined in: [index.ts:127](src/index.ts#L127)

the visible display name of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`visibleName`](EntryCommon.md#visiblename)

***

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:138](src/index.ts#L138)

the parent of this entry

There are two special parents, "" (empty string) for the root directory,
and "trash" for the trash

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`parent`](EntryCommon.md#parent)

***

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [index.ts:140](src/index.ts#L140)

any tags the entry might have

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`tags`](EntryCommon.md#tags)


---

<!-- source: interfaces/CPageNumberValue.md -->

[**rmapi-js**](../README.md)

***

# Interface: CPageNumberValue

Defined in: [raw.ts:180](src/raw.ts#L180)

a c-page value who's type is a string

## Properties

### timestamp

> **timestamp**: `string`

Defined in: [raw.ts:182](src/raw.ts#L182)

a pseudo-timestamp of the form "1:1" or "1:2"

***

### value

> **value**: `number`

Defined in: [raw.ts:184](src/raw.ts#L184)

the stored value


---

<!-- source: interfaces/CPagePage.md -->

[**rmapi-js**](../README.md)

***

# Interface: CPagePage

Defined in: [raw.ts:188](src/raw.ts#L188)

[speculative] information about an individual page

## Properties

### id

> **id**: `string`

Defined in: [raw.ts:190](src/raw.ts#L190)

[speculative] the page id

***

### idx

> **idx**: [`CPageStringValue`](CPageStringValue.md)

Defined in: [raw.ts:192](src/raw.ts#L192)

[unknown] values are like "aa", "ab", "ba", etc.

***

### deleted?

> `optional` **deleted**: [`CPageNumberValue`](CPageNumberValue.md)

Defined in: [raw.ts:202](src/raw.ts#L202)

[unknown]

***

### redir?

> `optional` **redir**: [`CPageNumberValue`](CPageNumberValue.md)

Defined in: [raw.ts:194](src/raw.ts#L194)

[unknown]

***

### scrollTime?

> `optional` **scrollTime**: [`CPageStringValue`](CPageStringValue.md)

Defined in: [raw.ts:198](src/raw.ts#L198)

[unknown] the value is a timestamp

***

### template?

> `optional` **template**: [`CPageStringValue`](CPageStringValue.md)

Defined in: [raw.ts:196](src/raw.ts#L196)

[speculative] the template name of the page

***

### verticalScroll?

> `optional` **verticalScroll**: [`CPageNumberValue`](CPageNumberValue.md)

Defined in: [raw.ts:200](src/raw.ts#L200)

[unknown]


---

<!-- source: interfaces/CPages.md -->

[**rmapi-js**](../README.md)

***

# Interface: CPages

Defined in: [raw.ts:271](src/raw.ts#L271)

[unknown] metadata about pages

## Properties

### lastOpened

> **lastOpened**: [`CPageStringValue`](CPageStringValue.md)

Defined in: [raw.ts:273](src/raw.ts#L273)

[speculative] the last time the document was opened

***

### original

> **original**: [`CPageNumberValue`](CPageNumberValue.md)

Defined in: [raw.ts:275](src/raw.ts#L275)

[unknown]

***

### pages

> **pages**: [`CPagePage`](CPagePage.md)[]

Defined in: [raw.ts:277](src/raw.ts#L277)

[speculative] information about individual pages

***

### uuids

> **uuids**: [`CPageUUID`](CPageUUID.md)[] \| `null`

Defined in: [raw.ts:279](src/raw.ts#L279)

[unknown]


---

<!-- source: interfaces/CPageStringValue.md -->

[**rmapi-js**](../README.md)

***

# Interface: CPageStringValue

Defined in: [raw.ts:172](src/raw.ts#L172)

a c-page value who's type is a string

## Properties

### timestamp

> **timestamp**: `string`

Defined in: [raw.ts:174](src/raw.ts#L174)

a pseudo-timestamp of the form "1:1" or "1:2"

***

### value

> **value**: `string`

Defined in: [raw.ts:176](src/raw.ts#L176)

the stored value


---

<!-- source: interfaces/CPageUUID.md -->

[**rmapi-js**](../README.md)

***

# Interface: CPageUUID

Defined in: [raw.ts:263](src/raw.ts#L263)

[unknown]

## Properties

### first

> **first**: `string`

Defined in: [raw.ts:265](src/raw.ts#L265)

[unknown]

***

### second

> **second**: `number`

Defined in: [raw.ts:267](src/raw.ts#L267)

[unknown]


---

<!-- source: interfaces/DocumentContent.md -->

[**rmapi-js**](../README.md)

***

# Interface: DocumentContent

Defined in: [raw.ts:337](src/raw.ts#L337)

content metadata, stored with the "content" extension

This largely contains description of how to render the document, rather than
metadata about it.

## Properties

### coverPageNumber

> **coverPageNumber**: `number`

Defined in: [raw.ts:343](src/raw.ts#L343)

which page to use for the thumbnail

-1 indicates the last visited page, whereas 0 is the first page.

***

### documentMetadata

> **documentMetadata**: [`DocumentMetadata`](DocumentMetadata.md)

Defined in: [raw.ts:345](src/raw.ts#L345)

metadata about the author, publishers, etc.

***

### extraMetadata

> **extraMetadata**: `Record`\<`string`, `string`\>

Defined in: [raw.ts:349](src/raw.ts#L349)

the largely contains metadata about what pens were used and their settings

***

### fileType

> **fileType**: [`FileType`](../type-aliases/FileType.md)

Defined in: [raw.ts:351](src/raw.ts#L351)

the underlying file type of this document

***

### fontName

> **fontName**: `string`

Defined in: [raw.ts:360](src/raw.ts#L360)

the name of the font to use for text rendering

The reMarkable supports five fonts by default: "Noto Sans", "Noto Sans UI",
"EB Garamond", "Noto Mono", and "Noto Serif". You can also set the font to
the empty string or omit it for the default.

***

### lineHeight

> **lineHeight**: `number`

Defined in: [raw.ts:372](src/raw.ts#L372)

the line height

The reMarkable uses three built-in line heights: 100, 150, 200, and
uses -1 to indicate the default line height, but heights outside of these
also work.

***

### orientation

> **orientation**: [`Orientation`](../type-aliases/Orientation.md)

Defined in: [raw.ts:382](src/raw.ts#L382)

the document orientation

***

### pageCount

> **pageCount**: `number`

Defined in: [raw.ts:386](src/raw.ts#L386)

the number of pages

***

### sizeInBytes

> **sizeInBytes**: `string`

Defined in: [raw.ts:394](src/raw.ts#L394)

ostensibly the size in bytes of the file, but this differs from other measurements

***

### textAlignment

> **textAlignment**: [`TextAlignment`](../type-aliases/TextAlignment.md)

Defined in: [raw.ts:398](src/raw.ts#L398)

text alignment for this document

***

### textScale

> **textScale**: `number`

Defined in: [raw.ts:405](src/raw.ts#L405)

the font size

reMarkable uses six built-in text scales: 0.7, 0.8, 1, 1.2, 1.5, 2, but
values outside of this range are valid.

***

### cPages?

> `optional` **cPages**: [`CPages`](CPages.md)

Defined in: [raw.ts:445](src/raw.ts#L445)

[speculative] various other page metadata

***

### customZoomCenterX?

> `optional` **customZoomCenterX**: `number`

Defined in: [raw.ts:414](src/raw.ts#L414)

the center of the zoom for customFit zoom

This is an absolute offset from the center of the page. Negative numbers
indicate shifted left and positive numbers indicate shifted right. The
units are relative to the document pixels, but it's not sure how the
document size is calculated.

***

### customZoomCenterY?

> `optional` **customZoomCenterY**: `number`

Defined in: [raw.ts:423](src/raw.ts#L423)

the center of the zoom for customFit documents

This is an absolute number relative to the top of the page. Negative
numbers indicate shifted up, while positive numbers indicate shifted down.
The units are relative to the document pixels, but it's not sure how the
document size is calculated.

***

### customZoomOrientation?

> `optional` **customZoomOrientation**: [`Orientation`](../type-aliases/Orientation.md)

Defined in: [raw.ts:425](src/raw.ts#L425)

this seems unused

***

### customZoomPageHeight?

> `optional` **customZoomPageHeight**: `number`

Defined in: [raw.ts:427](src/raw.ts#L427)

this seems unused

***

### customZoomPageWidth?

> `optional` **customZoomPageWidth**: `number`

Defined in: [raw.ts:429](src/raw.ts#L429)

this seems unused

***

### customZoomScale?

> `optional` **customZoomScale**: `number`

Defined in: [raw.ts:437](src/raw.ts#L437)

the scale for customFit documents

1 indicates no zoom, smaller numbers indicate zoomed out, larger numbers
indicate zoomed in. reMarkable generally allows setting this from 0.5 to 5,
but values outside that bound are still supported.

***

### dummyDocument?

> `optional` **dummyDocument**: `boolean`

Defined in: [raw.ts:347](src/raw.ts#L347)

It's not known what this field is for

***

### formatVersion?

> `optional` **formatVersion**: `number`

Defined in: [raw.ts:362](src/raw.ts#L362)

the format version, this should always be 1

***

### keyboardMetadata?

> `optional` **keyboardMetadata**: [`KeyboardMetadata`](KeyboardMetadata.md)

Defined in: [raw.ts:443](src/raw.ts#L443)

[speculative] metadata about keyboard use

***

### lastOpenedPage?

> `optional` **lastOpenedPage**: `number`

Defined in: [raw.ts:364](src/raw.ts#L364)

the last opened page, starts at zero

***

### margins?

> `optional` **margins**: `number`

Defined in: [raw.ts:380](src/raw.ts#L380)

the document margin in pixels

The reMarkable uses three built-in margins: 50, 125, 200, but other margins
are possible. The reMarkable used to default to margins of 180.

***

### originalPageCount?

> `optional` **originalPageCount**: `number`

Defined in: [raw.ts:384](src/raw.ts#L384)

this specifies the number of pages, it's not clear how this is different than pageCount

***

### pages?

> `optional` **pages**: `string`[] \| `null`

Defined in: [raw.ts:390](src/raw.ts#L390)

a list of the ids of each page in the document, or null when never opened

***

### pageTags?

> `optional` **pageTags**: [`PageTag`](PageTag.md)[]

Defined in: [raw.ts:388](src/raw.ts#L388)

the page tags for the document

***

### redirectionPageMap?

> `optional` **redirectionPageMap**: `number`[]

Defined in: [raw.ts:392](src/raw.ts#L392)

a mapping from page number to page id in pages

***

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [raw.ts:396](src/raw.ts#L396)

document tags for this document

***

### transform?

> `optional` **transform**: `Record`\<`"m11"` \| `"m12"` \| `"m13"` \| `"m21"` \| `"m22"` \| `"m23"` \| `"m31"` \| `"m32"` \| `"m33"`, `number`\>

Defined in: [raw.ts:441](src/raw.ts#L441)

[speculative] a transform matrix, a. la. css matrix transform

***

### viewBackgroundFilter?

> `optional` **viewBackgroundFilter**: [`BackgroundFilter`](../type-aliases/BackgroundFilter.md)

Defined in: [raw.ts:453](src/raw.ts#L453)

setting for the adaptive contrast filter

off has no background filter, best for images, full page applies the high
contrast filter to the entire page. If this is omitted, reMarkable will try
to apply the filter only to text areas.

***

### zoomMode?

> `optional` **zoomMode**: [`ZoomMode`](../type-aliases/ZoomMode.md)

Defined in: [raw.ts:439](src/raw.ts#L439)

what zoom mode is set for the page


---

<!-- source: interfaces/DocumentMetadata.md -->

[**rmapi-js**](../README.md)

***

# Interface: DocumentMetadata

Defined in: [raw.ts:141](src/raw.ts#L141)

document metadata stored in [Content](../type-aliases/Content.md)

## Properties

### authors?

> `optional` **authors**: `string`[]

Defined in: [raw.ts:143](src/raw.ts#L143)

a list of authors as a string

***

### publicationDate?

> `optional` **publicationDate**: `string`

Defined in: [raw.ts:147](src/raw.ts#L147)

the publication date as an ISO date or timestamp

***

### publisher?

> `optional` **publisher**: `string`

Defined in: [raw.ts:149](src/raw.ts#L149)

the publisher

***

### title?

> `optional` **title**: `string`

Defined in: [raw.ts:145](src/raw.ts#L145)

the title as a string


---

<!-- source: interfaces/DocumentType.md -->

[**rmapi-js**](../README.md)

***

# Interface: DocumentType

Defined in: [index.ts:150](src/index.ts#L150)

a file, referred to in the api as a document

## Extends

- [`EntryCommon`](EntryCommon.md)

## Properties

### fileType

> **fileType**: `"epub"` \| `"pdf"` \| `"notebook"`

Defined in: [index.ts:154](src/index.ts#L154)

the type of the file

***

### hash

> **hash**: `string`

Defined in: [index.ts:125](src/index.ts#L125)

the current hash of the state of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`hash`](EntryCommon.md#hash)

***

### id

> **id**: `string`

Defined in: [index.ts:123](src/index.ts#L123)

the document id, a uuid4

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`id`](EntryCommon.md#id)

***

### lastModified

> **lastModified**: `string`

Defined in: [index.ts:129](src/index.ts#L129)

the last modified timestamp

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`lastModified`](EntryCommon.md#lastmodified)

***

### lastOpened

> **lastOpened**: `string`

Defined in: [index.ts:156](src/index.ts#L156)

the timestamp of the last time this entry was opened

***

### pinned

> **pinned**: `boolean`

Defined in: [index.ts:131](src/index.ts#L131)

true if the entry is starred in most ui elements

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`pinned`](EntryCommon.md#pinned)

***

### type

> **type**: `"DocumentType"`

Defined in: [index.ts:152](src/index.ts#L152)

the key to identify this as a document

***

### visibleName

> **visibleName**: `string`

Defined in: [index.ts:127](src/index.ts#L127)

the visible display name of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`visibleName`](EntryCommon.md#visiblename)

***

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:138](src/index.ts#L138)

the parent of this entry

There are two special parents, "" (empty string) for the root directory,
and "trash" for the trash

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`parent`](EntryCommon.md#parent)

***

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [index.ts:140](src/index.ts#L140)

any tags the entry might have

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`tags`](EntryCommon.md#tags)


---

<!-- source: interfaces/Entries.md -->

[**rmapi-js**](../README.md)

***

# Interface: Entries

Defined in: [raw.ts:79](src/raw.ts#L79)

a parsed entries file

id and size are defined for schema 4 but not for 3

## Properties

### entries

> **entries**: [`RawEntry`](RawEntry.md)[]

Defined in: [raw.ts:81](src/raw.ts#L81)

the raw entries in the file

***

### id?

> `optional` **id**: `string`

Defined in: [raw.ts:83](src/raw.ts#L83)

the id of this entry, only specified for schema 4

***

### size?

> `optional` **size**: `number`

Defined in: [raw.ts:85](src/raw.ts#L85)

the recursive size of this entry, only specified for schema 4


---

<!-- source: interfaces/EntryCommon.md -->

[**rmapi-js**](../README.md)

***

# Interface: EntryCommon

Defined in: [index.ts:121](src/index.ts#L121)

common properties shared by collections and documents

## Extended by

- [`CollectionEntry`](CollectionEntry.md)
- [`DocumentType`](DocumentType.md)
- [`TemplateType`](TemplateType.md)

## Properties

### hash

> **hash**: `string`

Defined in: [index.ts:125](src/index.ts#L125)

the current hash of the state of this entry

***

### id

> **id**: `string`

Defined in: [index.ts:123](src/index.ts#L123)

the document id, a uuid4

***

### lastModified

> **lastModified**: `string`

Defined in: [index.ts:129](src/index.ts#L129)

the last modified timestamp

***

### pinned

> **pinned**: `boolean`

Defined in: [index.ts:131](src/index.ts#L131)

true if the entry is starred in most ui elements

***

### visibleName

> **visibleName**: `string`

Defined in: [index.ts:127](src/index.ts#L127)

the visible display name of this entry

***

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:138](src/index.ts#L138)

the parent of this entry

There are two special parents, "" (empty string) for the root directory,
and "trash" for the trash

***

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [index.ts:140](src/index.ts#L140)

any tags the entry might have


---

<!-- source: interfaces/FolderOptions.md -->

[**rmapi-js**](../README.md)

***

# Interface: FolderOptions

Defined in: [index.ts:187](src/index.ts#L187)

options for creating a folder

## Properties

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:189](src/index.ts#L189)

the id of the folder's parent directory, "" or omitted for root


---

<!-- source: interfaces/HashEntry.md -->

[**rmapi-js**](../README.md)

***

# Interface: HashEntry

Defined in: [index.ts:175](src/index.ts#L175)

the new hash of a modified entry

## Properties

### hash

> **hash**: `string`

Defined in: [index.ts:177](src/index.ts#L177)

the actual hash


---

<!-- source: interfaces/HashesEntry.md -->

[**rmapi-js**](../README.md)

***

# Interface: HashesEntry

Defined in: [index.ts:181](src/index.ts#L181)

the mapping from old hashes to new hashes after a bulk modify

## Properties

### hashes

> **hashes**: `Record`\<`string`, `string`\>

Defined in: [index.ts:183](src/index.ts#L183)

the mapping from old to new hashes


---

<!-- source: interfaces/KeyboardMetadata.md -->

[**rmapi-js**](../README.md)

***

# Interface: KeyboardMetadata

Defined in: [raw.ts:164](src/raw.ts#L164)

[speculative] metadata stored about keyboard interactions

## Properties

### count

> **count**: `number`

Defined in: [raw.ts:166](src/raw.ts#L166)

[unknown]

***

### timestamp

> **timestamp**: `number`

Defined in: [raw.ts:168](src/raw.ts#L168)

[unknown]


---

<!-- source: interfaces/Metadata.md -->

[**rmapi-js**](../README.md)

***

# Interface: Metadata

Defined in: [raw.ts:578](src/raw.ts#L578)

item level metadata

Stored with the extension "metadata".

## Properties

### lastModified

> **lastModified**: `string`

Defined in: [raw.ts:584](src/raw.ts#L584)

the last modify time, the string of the epoch timestamp

***

### parent

> **parent**: `string`

Defined in: [raw.ts:599](src/raw.ts#L599)

the id of the parent collection

This is the empty string for root (no parent), "trash" if it's in the
trash, or the id of the parent.

***

### pinned

> **pinned**: `boolean`

Defined in: [raw.ts:601](src/raw.ts#L601)

true of the item is starred

***

### type

> **type**: `"DocumentType"` \| `"CollectionType"` \| `"TemplateType"`

Defined in: [raw.ts:610](src/raw.ts#L610)

the type of item this corresponds to

DocumentType is a document, an epub, pdf, or notebook, CollectionType is a
folder.

***

### visibleName

> **visibleName**: `string`

Defined in: [raw.ts:622](src/raw.ts#L622)

the visible name of the item, what it's called on the reMarkable

***

### createdTime?

> `optional` **createdTime**: `string`

Defined in: [raw.ts:580](src/raw.ts#L580)

creation time, a string of the epoch timestamp

***

### deleted?

> `optional` **deleted**: `boolean`

Defined in: [raw.ts:582](src/raw.ts#L582)

[speculative] true if the item has been actually deleted

***

### lastOpened?

> `optional` **lastOpened**: `string`

Defined in: [raw.ts:586](src/raw.ts#L586)

the last opened epoch timestamp, isn't defined for CollectionType

***

### lastOpenedPage?

> `optional` **lastOpenedPage**: `number`

Defined in: [raw.ts:588](src/raw.ts#L588)

the last page opened, isn't defined for CollectionType, starts at 0

***

### metadatamodified?

> `optional` **metadatamodified**: `boolean`

Defined in: [raw.ts:590](src/raw.ts#L590)

[speculative] true if the metadata has been modified

***

### modified?

> `optional` **modified**: `boolean`

Defined in: [raw.ts:592](src/raw.ts#L592)

[speculative] true if the item has been modified

***

### new?

> `optional` **new**: `boolean`

Defined in: [raw.ts:612](src/raw.ts#L612)

whether this is this a newly-installed template

***

### source?

> `optional` **source**: `string`

Defined in: [raw.ts:618](src/raw.ts#L618)

the provider from which this item was obtained/installed

Example: a template from "com.remarkable.methods".

***

### synced?

> `optional` **synced**: `boolean`

Defined in: [raw.ts:603](src/raw.ts#L603)

[unknown]

***

### version?

> `optional` **version**: `number`

Defined in: [raw.ts:620](src/raw.ts#L620)

[speculative] metadata version, always 0


---

<!-- source: interfaces/PageTag.md -->

[**rmapi-js**](../README.md)

***

# Interface: PageTag

Defined in: [raw.ts:106](src/raw.ts#L106)

a tag for individual pages

## Extends

- [`Tag`](Tag.md)

## Properties

### name

> **name**: `string`

Defined in: [raw.ts:91](src/raw.ts#L91)

the name of the tag

#### Inherited from

[`Tag`](Tag.md).[`name`](Tag.md#name)

***

### pageId

> **pageId**: `string`

Defined in: [raw.ts:108](src/raw.ts#L108)

the id of the page this is on

***

### timestamp

> **timestamp**: `number`

Defined in: [raw.ts:93](src/raw.ts#L93)

the timestamp when this tag was added

#### Inherited from

[`Tag`](Tag.md).[`timestamp`](Tag.md#timestamp)


---

<!-- source: interfaces/PutOptions.md -->

[**rmapi-js**](../README.md)

***

# Interface: PutOptions

Defined in: [index.ts:302](src/index.ts#L302)

options for putting a file onto reMarkable

This is a more customizable version of the options available when using the
simpler upload api. This comes with the risk that is uses lower level apis,
and therefore has more failure points.

## See

[\`Content\`](../type-aliases/Content.md) and [\`Metadata\`](Metadata.md) for more
information on what these fields correspond to

## Properties

### authors?

> `optional` **authors**: `string`[]

Defined in: [index.ts:315](src/index.ts#L315)

document metadata authors

***

### coverPageNumber?

> `optional` **coverPageNumber**: `number`

Defined in: [index.ts:313](src/index.ts#L313)

0 for first page, -1 for last visited

***

### extraMetadata?

> `optional` **extraMetadata**: `Record`\<`string`, `string`\>

Defined in: [index.ts:323](src/index.ts#L323)

extra metadata often in the form of pen choices

***

### fontName?

> `optional` **fontName**: `string`

Defined in: [index.ts:325](src/index.ts#L325)

the font to use for rendering

***

### lineHeight?

> `optional` **lineHeight**: `number`

Defined in: [index.ts:327](src/index.ts#L327)

the line height to render

***

### margins?

> `optional` **margins**: `number`

Defined in: [index.ts:329](src/index.ts#L329)

the margins to render

***

### orientation?

> `optional` **orientation**: [`Orientation`](../type-aliases/Orientation.md)

Defined in: [index.ts:331](src/index.ts#L331)

the document orientation

***

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:309](src/index.ts#L309)

the collection to put this in

The empty string ("") (default) is the root, "trash" is in the trash,
otherwise this should be the uuid of a collection item to place this in.

***

### pinned?

> `optional` **pinned**: `boolean`

Defined in: [index.ts:311](src/index.ts#L311)

true to star the item

***

### publicationDate?

> `optional` **publicationDate**: `string`

Defined in: [index.ts:319](src/index.ts#L319)

the publication date, as an ISO date or timestamp

***

### publisher?

> `optional` **publisher**: `string`

Defined in: [index.ts:321](src/index.ts#L321)

the publisher

***

### refresh?

> `optional` **refresh**: `boolean`

Defined in: [index.ts:350](src/index.ts#L350)

whether to refresh current file structure before putting

If you suspect that other changes have been made to the remarkable backend
between the last put and now, setting this to true will avoid a
[\`GenerationError\`](../classes/GenerationError.md), but will cause an unnecessary
GET request otherwise.

***

### tags?

> `optional` **tags**: `string`[]

Defined in: [index.ts:333](src/index.ts#L333)

the names of the tags to add

***

### textAlignment?

> `optional` **textAlignment**: [`TextAlignment`](../type-aliases/TextAlignment.md)

Defined in: [index.ts:335](src/index.ts#L335)

the document text alignment

***

### textScale?

> `optional` **textScale**: `number`

Defined in: [index.ts:337](src/index.ts#L337)

the text scale of the document

***

### title?

> `optional` **title**: `string`

Defined in: [index.ts:317](src/index.ts#L317)

document metadata tile, NOTE this is not visibleName

***

### viewBackgroundFilter?

> `optional` **viewBackgroundFilter**: [`BackgroundFilter`](../type-aliases/BackgroundFilter.md)

Defined in: [index.ts:341](src/index.ts#L341)

the contrast filter setting

***

### zoomMode?

> `optional` **zoomMode**: [`ZoomMode`](../type-aliases/ZoomMode.md)

Defined in: [index.ts:339](src/index.ts#L339)

the document zoom mode


---

<!-- source: interfaces/RawEntry.md -->

[**rmapi-js**](../README.md)

***

# Interface: RawEntry

Defined in: [raw.ts:58](src/raw.ts#L58)

the low-level entry corresponding to a collection of files

A collection could be for the root collection, or for an individual document,
which is often a collection of files. If an entry represents a collection of
files, the high level entry will have the same hash and id as the low-level
entry for that collection.

## Properties

### hash

> **hash**: `string`

Defined in: [raw.ts:62](src/raw.ts#L62)

the hash of the collection this points to

***

### id

> **id**: `string`

Defined in: [raw.ts:64](src/raw.ts#L64)

the unique id of the collection

***

### size

> **size**: `number`

Defined in: [raw.ts:68](src/raw.ts#L68)

the total size of everything in the collection

***

### subfiles

> **subfiles**: `number`

Defined in: [raw.ts:66](src/raw.ts#L66)

the number of subfiles

***

### type

> **type**: `0` \| `80000000`

Defined in: [raw.ts:60](src/raw.ts#L60)

80000000 for schema 3 collection type or 0 for schema 4 or schema 3 files or


---

<!-- source: interfaces/RawRemarkableApi.md -->

[**rmapi-js**](../README.md)

***

# Interface: RawRemarkableApi

Defined in: [raw.ts:756](src/raw.ts#L756)

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

### clearCache()

> **clearCache**(): `void`

Defined in: [raw.ts:920](src/raw.ts#L920)

completely clear the cache

#### Returns

`void`

***

### dumpCache()

> **dumpCache**(): `string`

Defined in: [raw.ts:917](src/raw.ts#L917)

dump the current cache to a string to preserve between session

#### Returns

`string`

a serialized version of the cache to pass to a new api instance

***

### getContent()

> **getContent**(`hash`): `Promise`\<[`Content`](../type-aliases/Content.md)\>

Defined in: [raw.ts:806](src/raw.ts#L806)

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

### getEntries()

> **getEntries**(`hash`): `Promise`\<[`Entries`](Entries.md)\>

Defined in: [raw.ts:795](src/raw.ts#L795)

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

### getHash()

> **getHash**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [raw.ts:773](src/raw.ts#L773)

get the raw binary data associated with a hash

#### Parameters

##### hash

`string`

the hash to get the data for

#### Returns

`Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

the data

***

### getMetadata()

> **getMetadata**(`hash`): `Promise`\<[`Metadata`](Metadata.md)\>

Defined in: [raw.ts:817](src/raw.ts#L817)

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

### getRootHash()

> **getRootHash**(): `Promise`\<\[`string`, `number`, [`SchemaVersion`](../type-aliases/SchemaVersion.md)\]\>

Defined in: [raw.ts:765](src/raw.ts#L765)

gets the root hash and the current generation

When calling `putRootHash`, you should pass the generation you got from
this call. That way you tell reMarkable you're updating the previous state.

#### Returns

`Promise`\<\[`string`, `number`, [`SchemaVersion`](../type-aliases/SchemaVersion.md)\]\>

the root hash and the current generation

***

### getText()

> **getText**(`hash`): `Promise`\<`string`\>

Defined in: [raw.ts:784](src/raw.ts#L784)

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

### putContent()

> **putContent**(`id`, `content`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:864](src/raw.ts#L864)

the same as [\`putText\`](#puttext) but with extra validation for Content

#### Parameters

##### id

`string`

##### content

[`Content`](../type-aliases/Content.md)

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

***

### putEntries()

> **putEntries**(`id`, `entries`, `schemaVersion`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:887](src/raw.ts#L887)

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

### putFile()

> **putFile**(`id`, `bytes`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:858](src/raw.ts#L858)

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

### putMetadata()

> **putMetadata**(`id`, `metadata`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:867](src/raw.ts#L867)

the same as [\`putText\`](#puttext) but with extra validation for Metadata

#### Parameters

##### id

`string`

##### metadata

[`Metadata`](Metadata.md)

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

***

### putRootHash()

> **putRootHash**(`hash`, `generation`, `broadcast?`): `Promise`\<\[`string`, `number`\]\>

Defined in: [raw.ts:838](src/raw.ts#L838)

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

### putText()

> **putText**(`id`, `content`): `Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

Defined in: [raw.ts:861](src/raw.ts#L861)

the same as [\`putFile\`](#putfile) but with caching for text

#### Parameters

##### id

`string`

##### content

`string`

#### Returns

`Promise`\<\[[`RawEntry`](RawEntry.md), `Promise`\<`void`\>\]\>

***

### uploadFile()

> **uploadFile**(`visibleName`, `bytes`, `mime`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [raw.ts:906](src/raw.ts#L906)

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


---

<!-- source: interfaces/RegisterOptions.md -->

[**rmapi-js**](../README.md)

***

# Interface: RegisterOptions

Defined in: [index.ts:226](src/index.ts#L226)

options for registering with the api

## Properties

### authHost?

> `optional` **authHost**: `string`

Defined in: [index.ts:246](src/index.ts#L246)

The host to use for authorization requests

***

### deviceDesc?

> `optional` **deviceDesc**: `"desktop-windows"` \| `"desktop-macos"` \| `"desktop-linux"` \| `"mobile-android"` \| `"mobile-ios"` \| `"browser-chrome"` \| `"remarkable"`

Defined in: [index.ts:232](src/index.ts#L232)

the device description to use

Using an improper one will results in the registration being rejected.

***

### uuid?

> `optional` **uuid**: `string`

Defined in: [index.ts:244](src/index.ts#L244)

the unique id of this device

If omitted it will be randomly generated


---

<!-- source: interfaces/RemarkableApi.md -->

[**rmapi-js**](../README.md)

***

# Interface: RemarkableApi

Defined in: [index.ts:369](src/index.ts#L369)

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

### raw

> **raw**: [`RawRemarkableApi`](RawRemarkableApi.md)

Defined in: [index.ts:371](src/index.ts#L371)

scoped access to the raw low-level api

## Methods

### bulkDelete()

> **bulkDelete**(`hashes`, `refresh?`): `Promise`\<[`HashesEntry`](HashesEntry.md)\>

Defined in: [index.ts:685](src/index.ts#L685)

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

### bulkMove()

> **bulkMove**(`hashes`, `parent`, `refresh?`): `Promise`\<[`HashesEntry`](HashesEntry.md)\>

Defined in: [index.ts:669](src/index.ts#L669)

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

### clearCache()

> **clearCache**(): `void`

Defined in: [index.ts:721](src/index.ts#L721)

completely delete the cache

If the cache is causing memory issues, you can clear it, but this will hurt
performance.

#### Returns

`void`

***

### delete()

> **delete**(`hash`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:628](src/index.ts#L628)

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

### dumpCache()

> **dumpCache**(): `string`

Defined in: [index.ts:696](src/index.ts#L696)

get the current cache value as a string

You can use this to warm start a new instance of
[\`remarkable\`](../functions/remarkable.md) with any previously cached results.

#### Returns

`string`

***

### getContent()

> **getContent**(`hash`): `Promise`\<[`Content`](../type-aliases/Content.md)\>

Defined in: [index.ts:415](src/index.ts#L415)

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

### getDocument()

> **getDocument**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [index.ts:469](src/index.ts#L469)

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

### getEpub()

> **getEpub**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [index.ts:453](src/index.ts#L453)

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

### getMetadata()

> **getMetadata**(`hash`): `Promise`\<[`Metadata`](Metadata.md)\>

Defined in: [index.ts:431](src/index.ts#L431)

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

### getPdf()

> **getPdf**(`hash`): `Promise`\<`Uint8Array`\<`ArrayBufferLike`\>\>

Defined in: [index.ts:442](src/index.ts#L442)

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

### listIds()

> **listIds**(`refresh?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)[]\>

Defined in: [index.ts:399](src/index.ts#L399)

similar to [\`listItems\`](#listitems) but backed by the low level api

#### Parameters

##### refresh?

`boolean`

if true, refresh the root hash before listing

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)[]\>

***

### listItems()

> **listItems**(`refresh?`): `Promise`\<[`Entry`](../type-aliases/Entry.md)[]\>

Defined in: [index.ts:392](src/index.ts#L392)

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

### move()

> **move**(`hash`, `parent`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:617](src/index.ts#L617)

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

### pruneCache()

> **pruneCache**(`refresh?`): `Promise`\<`void`\>

Defined in: [index.ts:713](src/index.ts#L713)

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

### putEpub()

> **putEpub**(`visibleName`, `buffer`, `opts?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:507](src/index.ts#L507)

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

### putFolder()

> **putFolder**(`visibleName`, `opts?`, `refresh?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:514](src/index.ts#L514)

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

### putPdf()

> **putPdf**(`visibleName`, `buffer`, `opts?`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:486](src/index.ts#L486)

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

### rename()

> **rename**(`hash`, `visibleName`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:640](src/index.ts#L640)

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

### stared()

> **stared**(`hash`, `stared`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:656](src/index.ts#L656)

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

### updateCollection()

> **updateCollection**(`hash`, `content`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:583](src/index.ts#L583)

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

### updateDocument()

> **updateDocument**(`hash`, `content`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:566](src/index.ts#L566)

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

### updateTemplate()

> **updateTemplate**(`hash`, `content`, `refresh?`): `Promise`\<[`HashEntry`](HashEntry.md)\>

Defined in: [index.ts:600](src/index.ts#L600)

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

### uploadEpub()

> **uploadEpub**(`visibleName`, `buffer`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:534](src/index.ts#L534)

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

### uploadFolder()

> **uploadFolder**(`visibleName`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:553](src/index.ts#L553)

create a folder using the simple api

#### Parameters

##### visibleName

`string`

#### Returns

`Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

***

### uploadPdf()

> **uploadPdf**(`visibleName`, `buffer`): `Promise`\<[`SimpleEntry`](SimpleEntry.md)\>

Defined in: [index.ts:550](src/index.ts#L550)

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


---

<!-- source: interfaces/RemarkableOptions.md -->

[**rmapi-js**](../README.md)

***

# Interface: RemarkableOptions

Defined in: [index.ts:1511](src/index.ts#L1511)

options for a remarkable instance

## Extends

- [`AuthOptions`](AuthOptions.md).[`RemarkableSessionOptions`](RemarkableSessionOptions.md)

## Properties

### authHost?

> `optional` **authHost**: `string`

Defined in: [index.ts:1464](src/index.ts#L1464)

the url for making authorization requests

#### Default Value

```ts
"https://webapp-prod.cloud.remarkable.engineering"
```

#### Inherited from

[`AuthOptions`](AuthOptions.md).[`authHost`](AuthOptions.md#authhost)

***

### cache?

> `optional` **cache**: `string`

Defined in: [index.ts:1496](src/index.ts#L1496)

an initial cache value

Generated from calling [\`dumpCache\`](RemarkableApi.md#dumpcache) on a previous
instance.

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`cache`](RemarkableSessionOptions.md#cache)

***

### maxCacheSize?

> `optional` **maxCacheSize**: `number`

Defined in: [index.ts:1507](src/index.ts#L1507)

the maximum size of the cache in terms of total string length

By the JavaScript specification there are two bytes per character, but the
total memory usage of the cache will also be larger than just the size of
the data stored.

#### Default Value

```ts
Infinity
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`maxCacheSize`](RemarkableSessionOptions.md#maxcachesize)

***

### rawHost?

> `optional` **rawHost**: `string`

Defined in: [index.ts:1488](src/index.ts#L1488)

the url for making requests using the low-level api

#### Default Value

```ts
"https://eu.tectonic.remarkable.com"
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`rawHost`](RemarkableSessionOptions.md#rawhost)

***

### syncHost?

> `optional` **syncHost**: `string`

Defined in: [index.ts:1474](src/index.ts#L1474)

the url for making synchronization requests

#### Default Value

```ts
"https://web.eu.tectonic.remarkable.com"
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`syncHost`](RemarkableSessionOptions.md#synchost)

***

### uploadHost?

> `optional` **uploadHost**: `string`

Defined in: [index.ts:1481](src/index.ts#L1481)

the base url for making upload requests

#### Default Value

```ts
"https://internal.cloud.remarkable.com"
```

#### Inherited from

[`RemarkableSessionOptions`](RemarkableSessionOptions.md).[`uploadHost`](RemarkableSessionOptions.md#uploadhost)


---

<!-- source: interfaces/RemarkableSessionOptions.md -->

[**rmapi-js**](../README.md)

***

# Interface: RemarkableSessionOptions

Defined in: [index.ts:1468](src/index.ts#L1468)

options for constructing an api instance from a session token

## Extended by

- [`RemarkableOptions`](RemarkableOptions.md)

## Properties

### cache?

> `optional` **cache**: `string`

Defined in: [index.ts:1496](src/index.ts#L1496)

an initial cache value

Generated from calling [\`dumpCache\`](RemarkableApi.md#dumpcache) on a previous
instance.

***

### maxCacheSize?

> `optional` **maxCacheSize**: `number`

Defined in: [index.ts:1507](src/index.ts#L1507)

the maximum size of the cache in terms of total string length

By the JavaScript specification there are two bytes per character, but the
total memory usage of the cache will also be larger than just the size of
the data stored.

#### Default Value

```ts
Infinity
```

***

### rawHost?

> `optional` **rawHost**: `string`

Defined in: [index.ts:1488](src/index.ts#L1488)

the url for making requests using the low-level api

#### Default Value

```ts
"https://eu.tectonic.remarkable.com"
```

***

### syncHost?

> `optional` **syncHost**: `string`

Defined in: [index.ts:1474](src/index.ts#L1474)

the url for making synchronization requests

#### Default Value

```ts
"https://web.eu.tectonic.remarkable.com"
```

***

### uploadHost?

> `optional` **uploadHost**: `string`

Defined in: [index.ts:1481](src/index.ts#L1481)

the base url for making upload requests

#### Default Value

```ts
"https://internal.cloud.remarkable.com"
```


---

<!-- source: interfaces/SimpleEntry.md -->

[**rmapi-js**](../README.md)

***

# Interface: SimpleEntry

Defined in: [raw.ts:43](src/raw.ts#L43)

an simple entry without any extra information

## Properties

### hash

> **hash**: `string`

Defined in: [raw.ts:47](src/raw.ts#L47)

the document hash

***

### id

> **id**: `string`

Defined in: [raw.ts:45](src/raw.ts#L45)

the document id


---

<!-- source: interfaces/Tag.md -->

[**rmapi-js**](../README.md)

***

# Interface: Tag

Defined in: [raw.ts:89](src/raw.ts#L89)

a tag for an entry

## Extended by

- [`PageTag`](PageTag.md)

## Properties

### name

> **name**: `string`

Defined in: [raw.ts:91](src/raw.ts#L91)

the name of the tag

***

### timestamp

> **timestamp**: `number`

Defined in: [raw.ts:93](src/raw.ts#L93)

the timestamp when this tag was added


---

<!-- source: interfaces/TemplateContent.md -->

[**rmapi-js**](../README.md)

***

# Interface: TemplateContent

Defined in: [raw.ts:522](src/raw.ts#L522)

content metadata, stored with the "content" extension

This largely contains description of how to render the document, rather than
metadata about it.

## Properties

### author

> **author**: `string`

Defined in: [raw.ts:526](src/raw.ts#L526)

the template's author

***

### categories

> **categories**: `string`[]

Defined in: [raw.ts:530](src/raw.ts#L530)

category names this template belongs to (eg: "Planning", "Productivity")

***

### iconData

> **iconData**: `string`

Defined in: [raw.ts:528](src/raw.ts#L528)

Base64-encoded SVG icon image

***

### items

> **items**: `object`[]

Defined in: [raw.ts:549](src/raw.ts#L549)

the template definition, an SVG-like DSL in JSON

***

### labels

> **labels**: `string`[]

Defined in: [raw.ts:532](src/raw.ts#L532)

labels associated with this template (eg: "Project management")

***

### name

> **name**: `string`

Defined in: [raw.ts:524](src/raw.ts#L524)

the template name

***

### orientation

> **orientation**: `"portrait"` \| `"landscape"`

Defined in: [raw.ts:534](src/raw.ts#L534)

the orientation of this template

***

### supportedScreens

> **supportedScreens**: (`"rm2"` \| `"rmPP"`)[]

Defined in: [raw.ts:545](src/raw.ts#L545)

which screens the template supports:

- `rm2`: reMarkable 2
- `rmPP`: reMarkable Paper Pro

***

### templateVersion

> **templateVersion**: `string`

Defined in: [raw.ts:536](src/raw.ts#L536)

semantic version for this template

***

### constants?

> `optional` **constants**: `object`[]

Defined in: [raw.ts:547](src/raw.ts#L547)

constant values used by the commands in `items`

#### Index Signature

\[`name`: `string`\]: `number`

***

### formatVersion?

> `optional` **formatVersion**: `number`

Defined in: [raw.ts:538](src/raw.ts#L538)

template configuration format version (currently just `1`)


---

<!-- source: interfaces/TemplateType.md -->

[**rmapi-js**](../README.md)

***

# Interface: TemplateType

Defined in: [index.ts:160](src/index.ts#L160)

a template, such as from methods.remarkable.com

## Extends

- [`EntryCommon`](EntryCommon.md)

## Properties

### hash

> **hash**: `string`

Defined in: [index.ts:125](src/index.ts#L125)

the current hash of the state of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`hash`](EntryCommon.md#hash)

***

### id

> **id**: `string`

Defined in: [index.ts:123](src/index.ts#L123)

the document id, a uuid4

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`id`](EntryCommon.md#id)

***

### lastModified

> **lastModified**: `string`

Defined in: [index.ts:129](src/index.ts#L129)

the last modified timestamp

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`lastModified`](EntryCommon.md#lastmodified)

***

### pinned

> **pinned**: `boolean`

Defined in: [index.ts:131](src/index.ts#L131)

true if the entry is starred in most ui elements

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`pinned`](EntryCommon.md#pinned)

***

### type

> **type**: `"TemplateType"`

Defined in: [index.ts:162](src/index.ts#L162)

the key to identify this as a template

***

### visibleName

> **visibleName**: `string`

Defined in: [index.ts:127](src/index.ts#L127)

the visible display name of this entry

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`visibleName`](EntryCommon.md#visiblename)

***

### createdTime?

> `optional` **createdTime**: `string`

Defined in: [index.ts:164](src/index.ts#L164)

the timestamp of when the template was added/created

***

### new?

> `optional` **new**: `boolean`

Defined in: [index.ts:168](src/index.ts#L168)

indicates if this is a newly-installed template

***

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:138](src/index.ts#L138)

the parent of this entry

There are two special parents, "" (empty string) for the root directory,
and "trash" for the trash

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`parent`](EntryCommon.md#parent)

***

### source?

> `optional` **source**: `string`

Defined in: [index.ts:166](src/index.ts#L166)

where this template was installed from

***

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [index.ts:140](src/index.ts#L140)

any tags the entry might have

#### Inherited from

[`EntryCommon`](EntryCommon.md).[`tags`](EntryCommon.md#tags)


---

<!-- source: README.md -->

**rmapi-js**

***

# rmapi-js

Create and interact with reMarkable cloud.

After getting a device token with the [\`register\`](functions/register.md) method,
persist it and create api instances using [\`remarkable\`](functions/remarkable.md).
Outside of registration, all relevant methods are in
[\`RemarkableApi\`](interfaces/RemarkableApi.md), or it's interior
[\`RawRemarkableApi\`](interfaces/RawRemarkableApi.md) (for lower level functions).

## Examples

A simple rename
```ts
import { register, remarkable } from "rmapi-js";

const code = "..."  // eight letter code from https://my.remarkable.com/device/browser/connect
const token = await register(code)
// persist token
const api = await remarkable(token);
// list all items (documents and collections)
const [first, ...rest] = api.listItems();
// rename first item
const entry = api.rename(first.hash, "new name");
```

A simple upload
```ts
import { remarkable } from "rmapi-js";

const api = await remarkable(...);
const entry = await api.putEpub("document name", epubBuffer);
```

## Remarks

The cloud api is essentially a collection of entries. Each entry has an id,
which is a uuid4 and a hash, which indicates it's current state, and changes
as the item mutates, where the id is constant. Most mutable operations take
the initial hash so that merge conflicts can be resolved. Each entry has a
number of properties, but a key property is the `parent`, which represents
its parent in the file structure. This will be another document id, or one of
two special ids, "" (the empty string) for the root directory, or "trash" for
the trash.

Detailed information about the low-level storage an apis can be found in
[\`RawRemarkableApi\`](interfaces/RawRemarkableApi.md).

Additionally, this entire api was reverse engineered, so some things are only
`[speculative]`, or entirely `[unknown]`. If something breaks, please
[file an issue!](https://github.com/erikbrinkman/rmapi-js/issues)

## Classes

- [GenerationError](classes/GenerationError.md)
- [HashNotFoundError](classes/HashNotFoundError.md)
- [ResponseError](classes/ResponseError.md)
- [ValidationError](classes/ValidationError.md)

## Interfaces

- [AuthOptions](interfaces/AuthOptions.md)
- [CollectionContent](interfaces/CollectionContent.md)
- [CollectionEntry](interfaces/CollectionEntry.md)
- [CPageNumberValue](interfaces/CPageNumberValue.md)
- [CPagePage](interfaces/CPagePage.md)
- [CPages](interfaces/CPages.md)
- [CPageStringValue](interfaces/CPageStringValue.md)
- [CPageUUID](interfaces/CPageUUID.md)
- [DocumentContent](interfaces/DocumentContent.md)
- [DocumentMetadata](interfaces/DocumentMetadata.md)
- [DocumentType](interfaces/DocumentType.md)
- [Entries](interfaces/Entries.md)
- [EntryCommon](interfaces/EntryCommon.md)
- [FolderOptions](interfaces/FolderOptions.md)
- [HashEntry](interfaces/HashEntry.md)
- [HashesEntry](interfaces/HashesEntry.md)
- [KeyboardMetadata](interfaces/KeyboardMetadata.md)
- [Metadata](interfaces/Metadata.md)
- [PageTag](interfaces/PageTag.md)
- [PutOptions](interfaces/PutOptions.md)
- [RawEntry](interfaces/RawEntry.md)
- [RawRemarkableApi](interfaces/RawRemarkableApi.md)
- [RegisterOptions](interfaces/RegisterOptions.md)
- [RemarkableApi](interfaces/RemarkableApi.md)
- [RemarkableOptions](interfaces/RemarkableOptions.md)
- [RemarkableSessionOptions](interfaces/RemarkableSessionOptions.md)
- [SimpleEntry](interfaces/SimpleEntry.md)
- [Tag](interfaces/Tag.md)
- [TemplateContent](interfaces/TemplateContent.md)
- [TemplateType](interfaces/TemplateType.md)

## Type Aliases

- [BackgroundFilter](type-aliases/BackgroundFilter.md)
- [Content](type-aliases/Content.md)
- [Entry](type-aliases/Entry.md)
- [FileType](type-aliases/FileType.md)
- [Orientation](type-aliases/Orientation.md)
- [SchemaVersion](type-aliases/SchemaVersion.md)
- [TextAlignment](type-aliases/TextAlignment.md)
- [UploadMimeType](type-aliases/UploadMimeType.md)
- [ZoomMode](type-aliases/ZoomMode.md)

## Functions

- [auth](functions/auth.md)
- [register](functions/register.md)
- [remarkable](functions/remarkable.md)
- [session](functions/session.md)


---

<!-- source: type-aliases/BackgroundFilter.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: BackgroundFilter

> **BackgroundFilter** = `"off"` \| `"fullpage"`

Defined in: [raw.ts:138](src/raw.ts#L138)

types of background filter

off has no background filter, best for images, full page applies the high
contrast filter to the entire page. If this is omitted, reMarkable will try
to apply the filter only to text areas.


---

<!-- source: type-aliases/Content.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: Content

> **Content** = [`CollectionContent`](../interfaces/CollectionContent.md) \| [`DocumentContent`](../interfaces/DocumentContent.md) \| [`TemplateContent`](../interfaces/TemplateContent.md)

Defined in: [raw.ts:571](src/raw.ts#L571)

content metadata for any item


---

<!-- source: type-aliases/Entry.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: Entry

> **Entry** = [`CollectionEntry`](../interfaces/CollectionEntry.md) \| [`DocumentType`](../interfaces/DocumentType.md) \| [`TemplateType`](../interfaces/TemplateType.md)

Defined in: [index.ts:172](src/index.ts#L172)

a remarkable entry for cloud items


---

<!-- source: type-aliases/FileType.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: FileType

> **FileType** = `"epub"` \| `"pdf"` \| `"notebook"`

Defined in: [raw.ts:72](src/raw.ts#L72)

the type of files reMarkable supports


---

<!-- source: type-aliases/Orientation.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: Orientation

> **Orientation** = `"portrait"` \| `"landscape"`

Defined in: [raw.ts:122](src/raw.ts#L122)

all supported document orientations


---

<!-- source: type-aliases/SchemaVersion.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: SchemaVersion

> **SchemaVersion** = `3` \| `4`

Defined in: [raw.ts:40](src/raw.ts#L40)

the schema version


---

<!-- source: type-aliases/TextAlignment.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: TextAlignment

> **TextAlignment** = `""` \| `"justify"` \| `"left"`

Defined in: [raw.ts:125](src/raw.ts#L125)

all supported text alignments


---

<!-- source: type-aliases/UploadMimeType.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: UploadMimeType

> **UploadMimeType** = `"application/pdf"` \| `"application/epub+zip"` \| `"folder"`

Defined in: [raw.ts:34](src/raw.ts#L34)

the supported upload mime types


---

<!-- source: type-aliases/ZoomMode.md -->

[**rmapi-js**](../README.md)

***

# Type Alias: ZoomMode

> **ZoomMode** = `"bestFit"` \| `"customFit"` \| `"fitToHeight"` \| `"fitToWidth"`

Defined in: [raw.ts:128](src/raw.ts#L128)

types of zoom modes for documents, applies primarily to pdf files