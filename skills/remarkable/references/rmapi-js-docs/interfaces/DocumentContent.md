[**rmapi-js**](../README.md)

***

# Interface: DocumentContent

Defined in: [raw.ts:337](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L337)

content metadata, stored with the "content" extension

This largely contains description of how to render the document, rather than
metadata about it.

## Properties

<a id="coverpagenumber"></a>

### coverPageNumber

> **coverPageNumber**: `number`

Defined in: [raw.ts:343](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L343)

which page to use for the thumbnail

-1 indicates the last visited page, whereas 0 is the first page.

***

<a id="documentmetadata"></a>

### documentMetadata

> **documentMetadata**: [`DocumentMetadata`](DocumentMetadata.md)

Defined in: [raw.ts:345](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L345)

metadata about the author, publishers, etc.

***

<a id="extrametadata"></a>

### extraMetadata

> **extraMetadata**: `Record`\<`string`, `string`\>

Defined in: [raw.ts:349](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L349)

the largely contains metadata about what pens were used and their settings

***

<a id="filetype"></a>

### fileType

> **fileType**: [`FileType`](../type-aliases/FileType.md)

Defined in: [raw.ts:351](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L351)

the underlying file type of this document

***

<a id="fontname"></a>

### fontName

> **fontName**: `string`

Defined in: [raw.ts:360](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L360)

the name of the font to use for text rendering

The reMarkable supports five fonts by default: "Noto Sans", "Noto Sans UI",
"EB Garamond", "Noto Mono", and "Noto Serif". You can also set the font to
the empty string or omit it for the default.

***

<a id="lineheight"></a>

### lineHeight

> **lineHeight**: `number`

Defined in: [raw.ts:372](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L372)

the line height

The reMarkable uses three built-in line heights: 100, 150, 200, and
uses -1 to indicate the default line height, but heights outside of these
also work.

***

<a id="orientation"></a>

### orientation

> **orientation**: [`Orientation`](../type-aliases/Orientation.md)

Defined in: [raw.ts:382](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L382)

the document orientation

***

<a id="pagecount"></a>

### pageCount

> **pageCount**: `number`

Defined in: [raw.ts:386](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L386)

the number of pages

***

<a id="sizeinbytes"></a>

### sizeInBytes

> **sizeInBytes**: `string`

Defined in: [raw.ts:394](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L394)

ostensibly the size in bytes of the file, but this differs from other measurements

***

<a id="textalignment"></a>

### textAlignment

> **textAlignment**: [`TextAlignment`](../type-aliases/TextAlignment.md)

Defined in: [raw.ts:398](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L398)

text alignment for this document

***

<a id="textscale"></a>

### textScale

> **textScale**: `number`

Defined in: [raw.ts:405](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L405)

the font size

reMarkable uses six built-in text scales: 0.7, 0.8, 1, 1.2, 1.5, 2, but
values outside of this range are valid.

***

<a id="cpages"></a>

### cPages?

> `optional` **cPages**: [`CPages`](CPages.md)

Defined in: [raw.ts:445](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L445)

[speculative] various other page metadata

***

<a id="customzoomcenterx"></a>

### customZoomCenterX?

> `optional` **customZoomCenterX**: `number`

Defined in: [raw.ts:414](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L414)

the center of the zoom for customFit zoom

This is an absolute offset from the center of the page. Negative numbers
indicate shifted left and positive numbers indicate shifted right. The
units are relative to the document pixels, but it's not sure how the
document size is calculated.

***

<a id="customzoomcentery"></a>

### customZoomCenterY?

> `optional` **customZoomCenterY**: `number`

Defined in: [raw.ts:423](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L423)

the center of the zoom for customFit documents

This is an absolute number relative to the top of the page. Negative
numbers indicate shifted up, while positive numbers indicate shifted down.
The units are relative to the document pixels, but it's not sure how the
document size is calculated.

***

<a id="customzoomorientation"></a>

### customZoomOrientation?

> `optional` **customZoomOrientation**: [`Orientation`](../type-aliases/Orientation.md)

Defined in: [raw.ts:425](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L425)

this seems unused

***

<a id="customzoompageheight"></a>

### customZoomPageHeight?

> `optional` **customZoomPageHeight**: `number`

Defined in: [raw.ts:427](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L427)

this seems unused

***

<a id="customzoompagewidth"></a>

### customZoomPageWidth?

> `optional` **customZoomPageWidth**: `number`

Defined in: [raw.ts:429](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L429)

this seems unused

***

<a id="customzoomscale"></a>

### customZoomScale?

> `optional` **customZoomScale**: `number`

Defined in: [raw.ts:437](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L437)

the scale for customFit documents

1 indicates no zoom, smaller numbers indicate zoomed out, larger numbers
indicate zoomed in. reMarkable generally allows setting this from 0.5 to 5,
but values outside that bound are still supported.

***

<a id="dummydocument"></a>

### dummyDocument?

> `optional` **dummyDocument**: `boolean`

Defined in: [raw.ts:347](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L347)

It's not known what this field is for

***

<a id="formatversion"></a>

### formatVersion?

> `optional` **formatVersion**: `number`

Defined in: [raw.ts:362](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L362)

the format version, this should always be 1

***

<a id="keyboardmetadata"></a>

### keyboardMetadata?

> `optional` **keyboardMetadata**: [`KeyboardMetadata`](KeyboardMetadata.md)

Defined in: [raw.ts:443](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L443)

[speculative] metadata about keyboard use

***

<a id="lastopenedpage"></a>

### lastOpenedPage?

> `optional` **lastOpenedPage**: `number`

Defined in: [raw.ts:364](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L364)

the last opened page, starts at zero

***

<a id="margins"></a>

### margins?

> `optional` **margins**: `number`

Defined in: [raw.ts:380](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L380)

the document margin in pixels

The reMarkable uses three built-in margins: 50, 125, 200, but other margins
are possible. The reMarkable used to default to margins of 180.

***

<a id="originalpagecount"></a>

### originalPageCount?

> `optional` **originalPageCount**: `number`

Defined in: [raw.ts:384](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L384)

this specifies the number of pages, it's not clear how this is different than pageCount

***

<a id="pages"></a>

### pages?

> `optional` **pages**: `string`[] \| `null`

Defined in: [raw.ts:390](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L390)

a list of the ids of each page in the document, or null when never opened

***

<a id="pagetags"></a>

### pageTags?

> `optional` **pageTags**: [`PageTag`](PageTag.md)[]

Defined in: [raw.ts:388](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L388)

the page tags for the document

***

<a id="redirectionpagemap"></a>

### redirectionPageMap?

> `optional` **redirectionPageMap**: `number`[]

Defined in: [raw.ts:392](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L392)

a mapping from page number to page id in pages

***

<a id="tags"></a>

### tags?

> `optional` **tags**: [`Tag`](Tag.md)[]

Defined in: [raw.ts:396](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L396)

document tags for this document

***

<a id="transform"></a>

### transform?

> `optional` **transform**: `Record`\<`"m11"` \| `"m12"` \| `"m13"` \| `"m21"` \| `"m22"` \| `"m23"` \| `"m31"` \| `"m32"` \| `"m33"`, `number`\>

Defined in: [raw.ts:441](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L441)

[speculative] a transform matrix, a. la. css matrix transform

***

<a id="viewbackgroundfilter"></a>

### viewBackgroundFilter?

> `optional` **viewBackgroundFilter**: [`BackgroundFilter`](../type-aliases/BackgroundFilter.md)

Defined in: [raw.ts:453](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L453)

setting for the adaptive contrast filter

off has no background filter, best for images, full page applies the high
contrast filter to the entire page. If this is omitted, reMarkable will try
to apply the filter only to text areas.

***

<a id="zoommode"></a>

### zoomMode?

> `optional` **zoomMode**: [`ZoomMode`](../type-aliases/ZoomMode.md)

Defined in: [raw.ts:439](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L439)

what zoom mode is set for the page
