const Checkbox = ({ label, handleChange }) => {
  const [isChecked, setIsChecked] = React.useState(false);

  const toggleCheckboxChange = () => {
    setIsChecked(!isChecked);
    handleChange(label);
  }

  return (
    <div>
      <label>
        <input
          type='checkbox'
          value={label}
          checked={isChecked}
          onChange={toggleCheckboxChange}
          style={{
            'margin': '0 5px'
          }}
        />
        {label}
      </label>
    </div>
  );
};

const getCities = async () => {
  try {
    const res = await fetch('/api/get_column_distinct?column_name=city', {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const cities = await res.json();
    return cities;
  } catch (e) {
    console.error(e);
    return [];
  }
}

const selected = {};

const Cities = () => {
  const [cities, setCities] = React.useState([]);
  const [data, setData] = React.useState([]);
  const [selectedCities, setSelectedCities] = React.useState([]);
  const metricRef = React.createRef();
  const groupByRef = React.createRef();

  React.useEffect(async () => {
    const citiesList = await getCities();
    setCities(citiesList);
  }, []);

  if (!cities || cities.length === 0) {
    return (<div>Loading...</div>);
  }

  return (
    <div style={{ padding: '10px' }}>
      Please select cities:
      {cities.map((city, index) => {
        return (
          <Checkbox
            key={index}
            label={city}
            handleChange={() => {
              selected[city] = !selected[city];
            }}
          />
        );
      })}

      <label for="metrics">Select a metric:</label>
      <select id="metrics" ref={metricRef} style={{
        margin: '0 5px'
      }}>
        <option value="total_viewers">Total Viewers</option>
        <option value="average_viewers">Average Viewers</option>
      </select>

      <label for="group_by">Select a group:</label>
      <select id="group_by" ref={groupByRef} style={{
        margin: '0 5px'
      }}>
        <option value="genre">Program Genre</option>
        <option value="network">Program Network</option>
      </select>
      <div>
      <button
        onClick={() => {
          setSelectedCities(Object.keys(selected).filter((city) => selected[city]));
          fetch('/api/analyze_data', {
            headers: {
              'Content-Type': 'application/json'
            },
            method: 'POST',
            body: JSON.stringify({
              cities: Object.keys(selected).filter((city) => selected[city]),
              metrics: metricRef.current.value,
              group_by: groupByRef.current.value
            })
          })
          .then((res) => res.json())
          .then((data) => setData(data))
        }}
      >
        Submit
      </button>
      </div>
      {data && Object.keys(data).length > 0 && (
        <table>
          <thead>
            <th></th>
            {selectedCities.map((city, index) => (
              <th key={index}>{city}</th>
            ))}
          </thead>
          <tbody>
            {Object.keys(data).map((cat, index) => (
              <tr key={index}>
                <th>{cat}</th>
                {selectedCities.map((city, idx) => (
                  <td key={idx}>{data[cat][city]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

const App = () => {
  return <Cities />;
};

ReactDOM.render(<App />, document.getElementById('root'));
