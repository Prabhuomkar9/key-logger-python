import React, { useState, useEffect } from "react";

const App = () => {
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/logs")
      .then((response) => response.json())
      .then((data) => {
        setLogs(data);
        setFilteredLogs(data.slice(0, 25));
      });
  }, []);

  const prev = () => {
    const lastLogIndex = filteredLogs[0].id;
    const newLogs = logs.filter((log) => log.id < lastLogIndex);
    if (newLogs.length === 0) return;
    setFilteredLogs(newLogs.slice(0, 25));
  };

  const next = () => {
    const lastLogIndex = filteredLogs[filteredLogs.length - 1].id;
    const newLogs = logs.filter((log) => log.id > lastLogIndex);
    if (newLogs.length === 0) return;
    setFilteredLogs(newLogs.slice(0, 25));
  };

  return (
    <>
      <table
        style={{
          borderCollapse: "collapse",
          width: "90%",
          maxHeight: "90%",
        }}>
        <thead>
          <tr style={{ backgroundColor: "#f2f2f2" }}>
            <th style={tableCellStyle}>ID</th>
            <th style={tableCellStyle}>IP</th>
            <th style={tableCellStyle}>Logged At</th>
            <th style={tableCellStyle}>Key Pressed</th>
            <th style={tableCellStyle}>Is Key Down</th>
          </tr>
        </thead>
        <tbody>
          {filteredLogs.map((log, index) => (
            <tr key={index} style={tableCellStyle}>
              <td style={tableCellStyle}>{log.id}</td>
              <td style={tableCellStyle}>{log.ip}</td>
              <td style={tableCellStyle}>{log.loggedAt}</td>
              <td style={tableCellStyle}>{log.keyPressed}</td>
              <td
                style={{
                  ...tableCellStyle,
                  color: log.isKeyDown ? "green" : "red",
                }}>
                {log.isKeyDown ? "Yes" : "No"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: "100px",
        }}>
        <button
          style={{
            padding: "5px",
            borderRadius: "10px",
          }}
          onClick={prev}>
          Prev 25
        </button>
        <button
          style={{
            padding: "5px",
            borderRadius: "10px",
          }}
          onClick={next}>
          Next 25
        </button>
      </div>
    </>
  );
};

const tableCellStyle = {
  border: "1px solid #ddd",
  padding: "8px",
};

export default App;
