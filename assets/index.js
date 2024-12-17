
//   import _ from 'lodash';

// function component() {
//   const element = document.createElement('div');
//   element.innerHTML =  _.join(['Hello', 'lodash'], ' ');
//   return element;
// }
// document.body.appendChild(component());

// import React from 'react';
// import ReactDOM from "react-dom";

// ReactDOM.render(
//   <h1>Hello, react!</h1>,
//   document.getElementById('root')
// );

import React from 'react';
import ReactDOM from 'react-dom/client';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<h1>Hello, React!</h1>);