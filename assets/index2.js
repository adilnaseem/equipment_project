import React from 'react';
import ReactDOM from 'react-dom/client';
import EmployeeApplication from './App';
import { EmployeeList } from './App';
import axios from 'axios';
const root1 = ReactDOM.createRoot(document.getElementById('root1'));
root1.render(<h1>Hello I am Adil</h1>);
//  http://127.0.0.1:8000/api/employees/?format=json




const OpenAPIClientAxios = require("openapi-client-axios").default;
const api = new OpenAPIClientAxios({
  definition: "http://127.0.0.1:8000/api/", // Ensure this points to your OpenAPI spec
});
api
  .init()
  .then((client) => {
    return client.get('/api/employees'); // Adjust method name if necessary
  })
  .then((res) => {
    const root2 = ReactDOM.createRoot(document.getElementById('my-js'));
    root2.render(<EmployeeApplication result={res.data} />);
  })
  .catch((error) => {
    console.error("API call error:", error); // Handle any errors
  });
// fetch('/api/employees/')
//   .then(res => res.json())
//   .then(
//     (result) => {
//       // Assuming `client` is defined and has the employeesList method
//       const root2 = ReactDOM.createRoot(document.getElementById('my-js'));
//       root2.render(<EmployeeApplication client={client} />); // Pass client as a prop
//     },
//     (error) => {
//       console.error('Error loading employees:', error); // Log the error for debugging
//       const root2 = ReactDOM.createRoot(document.getElementById('my-js'));
//       root2.render(<h1>Error loading employees</h1>); // Display an error message
//     }
//   );

