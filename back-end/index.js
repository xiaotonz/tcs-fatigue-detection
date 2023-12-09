const config = require('./config');

const axios = require('axios');

const express = require('express');
const app = express();

const https = require('https');
const bodyParser = require('body-parser');
const cors = require('cors');

const mysql = require('mysql')
const connection = mysql.createConnection({
  host: 'tcs-fatigue-server.mysql.database.azure.com',
  user: 'tcsadmin',
  password: 'sql@server123',
  database: 'employee_db'
})

connection.connect()

app.use(express.json());
app.use(cors());
    
app.get('/', (req, res)=>{
    res.send('Returning processing response!')
});


app.get('/shift/shiftId/:shiftId', (req, res) => {
  
  const shiftId = req.params.shiftId;

  
  const sql = 'SELECT * FROM EMPLOYEE WHERE emp_shift = ?';

  const jsonRows = [];

  connection.query(sql, [shiftId], (err, rows, fields) => {
    if (err) {
      console.log(err);
    };
      // Create an array to store the JSON objects


  // Iterate through the rows and convert each RowDataPacket to a JSON object
  rows.forEach(row => {
    const jsonObject = {
      emp_id: row.emp_id,
      emp_name: row.emp_name,
      emp_position: row.emp_position,
      emp_shift: row.emp_shift
    };
    jsonRows.push(jsonObject);
  });

  
    // console.log('Result: ', jsonRows);
    res.send(jsonRows);
  });

});

app.get('/shift/shiftNumbers', (req, res) => {
  
  const sql = 'SELECT DISTINCT(emp_shift) FROM EMPLOYEE ';

  connection.query(sql,(err, rows) => { 
    if (err) {
      console.log(err);
    };
      // Create an array to store the JSON objects


    const jsonArray = rows.map(row => {
      return {
        emp_shift: row.emp_shift
      };
    });
    const extractedValues = jsonArray.map(obj => obj.emp_shift);

  
    // console.log('Result: ', jsonRows);
    res.send(extractedValues);
  });

});

app.get('/employee/empId/:empId', (req, res) => {
  
  const empId = req.params.empId;

  
  const sql = 'SELECT * FROM EMPLOYEE WHERE emp_id = ?';

  const jsonRows = [];

  connection.query(sql, [empId], (err, rows, fields) => {
    if (err) {
      console.log(err);
    };

      // Create an array to store the JSON objects


  // Iterate through the rows and convert each RowDataPacket to a JSON object
  rows.forEach(row => {
    const jsonObject = {
      emp_id: row.emp_id,
      emp_name: row.emp_name,
      emp_position: row.emp_position,
      emp_shift: row.emp_shift
    };
    jsonRows.push(jsonObject);
  });

  
    // console.log('Result: ', jsonRows);
    res.send(jsonRows);
  });



// You can use userId in your logic

});


app.get('/employee/list', (req, res) => {
  
  const sql ='select * from EMPLOYEE';

  const jsonRows = [];

  connection.query(sql,(err, rows) => { 
    if (err) {
      console.log(err);
    };
      // Create an array to store the JSON objects


  // Iterate through the rows and convert each RowDataPacket to a JSON object
  rows.forEach(row => {
    const jsonObject = {
      emp_id: row.emp_id,
      emp_name: row.emp_name
    };
    jsonRows.push(jsonObject);
  });

  
    // console.log('Result: ', jsonRows);
    res.send(jsonRows);
  });

});



app.get('/history/empId/:empId', (req, res) => {
  
  const empId = req.params.empId;

  
  const sql = 'SELECT * FROM FATIGUE_HISTORY WHERE emp_id = ?';

  const jsonRows = [];

  connection.query(sql, [empId], (err, rows, fields) => {
    if (err) {
      console.log(err);
    };
      // Create an array to store the JSON objects


  // Iterate through the rows and convert each RowDataPacket to a JSON object
  rows.forEach(row => {
    const jsonObject = {
      id: row.id,
      created_at: row.created_at,
      emp_id: row.emp_id
    };
    jsonRows.push(jsonObject);
  });

  
    // console.log('Result: ', jsonRows);
    res.send(jsonRows);
  });

});




app.get('/history/duration/:duration', (req, res) => {
  
  const duration = req.params.duration;   //can be week, fortnight, month
  var sql ='';

  if(duration.toLowerCase() == 'week')
    sql = 'SELECT * FROM FATIGUE_HISTORY WHERE DATE(created_at) >= DATE(NOW() - INTERVAL 7 DAY)';
  if(duration.toLowerCase() == 'fortnight') 
    sql = 'SELECT * FROM FATIGUE_HISTORY WHERE DATE(created_at) >= DATE(NOW() - INTERVAL 15 DAY)';
  if(duration.toLowerCase() == 'month') 
    sql = 'SELECT * FROM FATIGUE_HISTORY WHERE DATE(created_at) >= DATE(NOW() - INTERVAL 1 MONTH)';

  const jsonRows = [];

  connection.query(sql, (err, rows) => { 
    if (err) {
      console.log(err);
    };
      // Create an array to store the JSON objects


  // Iterate through the rows and convert each RowDataPacket to a JSON object
  rows.forEach(row => {
    const jsonObject = {
      id: row.id,
      created_at: row.created_at,
      emp_id: row.emp_id
    };
    jsonRows.push(jsonObject);
  });

  
    // console.log('Result: ', jsonRows);
    res.send(jsonRows);
  });

});


app.listen(config.PORT, ()=>{
    console.log('Application started successfully on port: ' + config.PORT);
});

