# TypeScript bindings for stake-pool program

For use with both node.js and in-browser.

## Installation

```
npm install
```

## Build and run

In the `js` folder:

```
npm run build
```

The build is available at `dist/index.js` (or `dist.browser/index.iife.js` in the browser).

## Browser bundle
```html
<!-- Development (un-minified) -->
<script src="https://unpkg.com/@trezoa/tpl-stake-pool@latest/dist.browser/index.iife.js"></script>

<!-- Production (minified) -->
<script src="https://unpkg.com/@trezoa/tpl-stake-pool@latest/dist.browser/index.iife.min.js"></script>
```

## Test

```
npm test
```

## Usage

### JavaScript
```javascript
const trezoaStakePool = require('@trezoa/tpl-stake-pool');
console.log(trezoaStakePool);
```

### ES6
```javascript
import * as trezoaStakePool from '@trezoa/tpl-stake-pool';
console.log(trezoaStakePool);
```

### Browser bundle
```javascript
// `trezoaStakePool` is provided in the global namespace by the script bundle.
console.log(trezoaStakePool);
```
