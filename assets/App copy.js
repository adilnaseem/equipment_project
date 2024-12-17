import React, { useState, useEffect } from 'react';

const EmployeeApplication = (props) => {
  const [isLoading, setIsLoading] = useState(true);
  const [employees, setEmployees] = useState([]);

  const client = props.client; // Change this to use props.client

  useEffect(() => {
    client.employeesList()
      .then((result) => {
        setEmployees(result.results); // Set employees from the fetched result
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching employees:", error);
        setIsLoading(false); // Stop loading even on error
      });
  }, [client]);

  if (isLoading) {
    return <p>Employee data is loading...</p>;
  }

  if (employees.length === 0) {
    return <p>No employees found!</p>;
  }

  return <EmployeeList employees={employees} />;
};

const EmployeeList = (props) => {
  console.log(props.employees.results);
  return (
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
          <th>Salary</th>
        </tr>
      </thead>
      <tbody>
        {props.employees.results.map((employee, index) => (
          <tr key={index}>
            <td>{employee.name}</td>
            <td>{employee.department}</td>
            <td>{employee.salary}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};



const AddEmployeeWidget = (props) => {
  const client = props.client;
  const [name, setName] = useState(props.name || '');
  const [department, setDepartment] = useState(props.department || '');
  const [salary, setSalary] = useState(props.salary || '');

  const saveEmployee = () => {
    const employee = {
      name,
      department,
      salary,
    };
    client.employeesCreate({ employee })
      .then((result) => {
        props.employeeSaved(result);
      })
      .catch((error) => {
        console.error("Error saving employee:", error);
      });
  };

  return (
    <section>
      <label>Name</label>
      <input
        type="text"
        placeholder="Michael Scott"
        onChange={(event) => setName(event.target.value)}
        value={name}
      />
      <label>Department</label>
      <select onChange={(event) => setDepartment(event.target.value)} value={department}>
        {DEPARTMENT_CHOICES.map((department, i) => (
          <option key={i} value={department.id}>{department.name}</option>
        ))}
      </select>
      <input
        type="number"
        placeholder="50000"
        onChange={(event) => setSalary(event.target.value)}
        value={salary}
      />
      <button type='button' onClick={saveEmployee}>
        Add Employee
      </button>
    </section>
  );
};
export default EmployeeApplication
export { AddEmployeeWidget, EmployeeList };
