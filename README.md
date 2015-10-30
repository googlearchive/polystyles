## On-the-fly Polymer style modules

https://poly-style.appspot.com is a web service to wrap existing stylesheets with
Polymer's [style module system](https://www.polymer-project.org/1.0/docs/devguide/styling.html#style-modules).

## Usage

**Example** - load a stylesheet

```html
<head>
  <link rel="import" href="bower_components/polymer/polymer.html">
  <link rel="import" href="https://poly-style.appspot.com?url=https://example.com/styles.css">
  <style is="custom-style" include="shared-styles"></style>
</head>
```

By default, the id "shared-styles" is used on the dom-module wrapper (e.g. `<dom-module id="shared-styles">`). You can change this with the `id` URL param. See example below.

**Example** - use a custom id

```html
<head>
  <link rel="import" href="bower_components/polymer/polymer.html">
  <link rel="import" href="https://poly-style.appspot.com?id=theme-styles&url=https://example.com/styles.css">
  <style is="custom-style" include="theme-styles"></style>
</head>
```

**Example** - element that uses a shared style

```html
<link rel="import" href="../polymer/polymer.html">
<link rel="import" href="https://poly-style.appspot.com?id=material-styles&url=https://example.com/styles.css">

<dom-module id="my-element">
  <template>
    <style include="material-styles">
      /* Optional - define extra styles using the same <style> tag. */
      :host {
        display: block;
      }
    </style>
    ...
  </template>
  <script>
    Polymer({is: 'my-element'});
  </script>
</dom-module>
```

**Example** - wrapping css text

    <link rel="import" href="https://poly-style.appspot.com?styles=%3Ahost%7Bdisplay%3Ablock%3B%7D">

produces:

```html
<dom-module id="shared-styles">
  <template>
    <style>
      :host{display:block;}
    </style>
  </template>
</dom-module>
```

**Note:** the `url` parameter trumps the `style` parameter if both are used together.

## Run tests

Install the [webtest framework](http://webtest.pythonpaste.org/en/latest/):

    pip install WebTest

In the main project folder, run the rest runner:

    python testrunner.py ~/google-cloud-sdk test/

The first argument is the location of your App Engine SDK. The second argument is
the path to the test folder.

## Report issues

File bugs and feature requests at https://github.com/PolymerLabs/polystyles.
