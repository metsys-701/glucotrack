function RecordList({ records, deleteRecord }) {

  if (records.length === 0) {
    return <p>No records found</p>;
  }

  return (
    <ul>

      {records.map((record) => (

        <li key={record.id}>

          {record.glucose_value} mg/dL — {record.note}

          <button
            style={{ marginLeft: "10px" }}
            onClick={() => deleteRecord(record.id)}
          >
            Delete
          </button>

        </li>

      ))}

    </ul>
  );
}

export default RecordList;