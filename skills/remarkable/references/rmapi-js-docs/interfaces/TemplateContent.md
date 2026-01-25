[**rmapi-js**](../README.md)

***

# Interface: TemplateContent

Defined in: [raw.ts:522](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L522)

content metadata, stored with the "content" extension

This largely contains description of how to render the document, rather than
metadata about it.

## Properties

<a id="author"></a>

### author

> **author**: `string`

Defined in: [raw.ts:526](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L526)

the template's author

***

<a id="categories"></a>

### categories

> **categories**: `string`[]

Defined in: [raw.ts:530](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L530)

category names this template belongs to (eg: "Planning", "Productivity")

***

<a id="icondata"></a>

### iconData

> **iconData**: `string`

Defined in: [raw.ts:528](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L528)

Base64-encoded SVG icon image

***

<a id="items"></a>

### items

> **items**: `object`[]

Defined in: [raw.ts:549](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L549)

the template definition, an SVG-like DSL in JSON

***

<a id="labels"></a>

### labels

> **labels**: `string`[]

Defined in: [raw.ts:532](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L532)

labels associated with this template (eg: "Project management")

***

<a id="name"></a>

### name

> **name**: `string`

Defined in: [raw.ts:524](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L524)

the template name

***

<a id="orientation"></a>

### orientation

> **orientation**: `"portrait"` \| `"landscape"`

Defined in: [raw.ts:534](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L534)

the orientation of this template

***

<a id="supportedscreens"></a>

### supportedScreens

> **supportedScreens**: (`"rm2"` \| `"rmPP"`)[]

Defined in: [raw.ts:545](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L545)

which screens the template supports:

- `rm2`: reMarkable 2
- `rmPP`: reMarkable Paper Pro

***

<a id="templateversion"></a>

### templateVersion

> **templateVersion**: `string`

Defined in: [raw.ts:536](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L536)

semantic version for this template

***

<a id="constants"></a>

### constants?

> `optional` **constants**: `object`[]

Defined in: [raw.ts:547](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L547)

constant values used by the commands in `items`

#### Index Signature

\[`name`: `string`\]: `number`

***

<a id="formatversion"></a>

### formatVersion?

> `optional` **formatVersion**: `number`

Defined in: [raw.ts:538](https://github.com/erikbrinkman/rmapi-js/blob/753b4f86fe235f64784043fb74b1516a5df39592/src/raw.ts#L538)

template configuration format version (currently just `1`)
