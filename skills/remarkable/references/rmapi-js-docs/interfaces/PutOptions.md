[**rmapi-js**](../README.md)

***

# Interface: PutOptions

Defined in: [index.ts:302](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L302)

options for putting a file onto reMarkable

This is a more customizable version of the options available when using the
simpler upload api. This comes with the risk that is uses lower level apis,
and therefore has more failure points.

## See

[\`Content\`](../type-aliases/Content.md) and [\`Metadata\`](Metadata.md) for more
information on what these fields correspond to

## Properties

<a id="authors"></a>

### authors?

> `optional` **authors**: `string`[]

Defined in: [index.ts:315](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L315)

document metadata authors

***

<a id="coverpagenumber"></a>

### coverPageNumber?

> `optional` **coverPageNumber**: `number`

Defined in: [index.ts:313](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L313)

0 for first page, -1 for last visited

***

<a id="extrametadata"></a>

### extraMetadata?

> `optional` **extraMetadata**: `Record`\<`string`, `string`\>

Defined in: [index.ts:323](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L323)

extra metadata often in the form of pen choices

***

<a id="fontname"></a>

### fontName?

> `optional` **fontName**: `string`

Defined in: [index.ts:325](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L325)

the font to use for rendering

***

<a id="lineheight"></a>

### lineHeight?

> `optional` **lineHeight**: `number`

Defined in: [index.ts:327](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L327)

the line height to render

***

<a id="margins"></a>

### margins?

> `optional` **margins**: `number`

Defined in: [index.ts:329](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L329)

the margins to render

***

<a id="orientation"></a>

### orientation?

> `optional` **orientation**: [`Orientation`](../type-aliases/Orientation.md)

Defined in: [index.ts:331](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L331)

the document orientation

***

<a id="parent"></a>

### parent?

> `optional` **parent**: `string`

Defined in: [index.ts:309](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L309)

the collection to put this in

The empty string ("") (default) is the root, "trash" is in the trash,
otherwise this should be the uuid of a collection item to place this in.

***

<a id="pinned"></a>

### pinned?

> `optional` **pinned**: `boolean`

Defined in: [index.ts:311](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L311)

true to star the item

***

<a id="publicationdate"></a>

### publicationDate?

> `optional` **publicationDate**: `string`

Defined in: [index.ts:319](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L319)

the publication date, as an ISO date or timestamp

***

<a id="publisher"></a>

### publisher?

> `optional` **publisher**: `string`

Defined in: [index.ts:321](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L321)

the publisher

***

<a id="refresh"></a>

### refresh?

> `optional` **refresh**: `boolean`

Defined in: [index.ts:350](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L350)

whether to refresh current file structure before putting

If you suspect that other changes have been made to the remarkable backend
between the last put and now, setting this to true will avoid a
[\`GenerationError\`](../classes/GenerationError.md), but will cause an unnecessary
GET request otherwise.

***

<a id="tags"></a>

### tags?

> `optional` **tags**: `string`[]

Defined in: [index.ts:333](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L333)

the names of the tags to add

***

<a id="textalignment"></a>

### textAlignment?

> `optional` **textAlignment**: [`TextAlignment`](../type-aliases/TextAlignment.md)

Defined in: [index.ts:335](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L335)

the document text alignment

***

<a id="textscale"></a>

### textScale?

> `optional` **textScale**: `number`

Defined in: [index.ts:337](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L337)

the text scale of the document

***

<a id="title"></a>

### title?

> `optional` **title**: `string`

Defined in: [index.ts:317](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L317)

document metadata tile, NOTE this is not visibleName

***

<a id="viewbackgroundfilter"></a>

### viewBackgroundFilter?

> `optional` **viewBackgroundFilter**: [`BackgroundFilter`](../type-aliases/BackgroundFilter.md)

Defined in: [index.ts:341](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L341)

the contrast filter setting

***

<a id="zoommode"></a>

### zoomMode?

> `optional` **zoomMode**: [`ZoomMode`](../type-aliases/ZoomMode.md)

Defined in: [index.ts:339](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/index.ts#L339)

the document zoom mode
