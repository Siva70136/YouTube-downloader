import { useState } from 'react';
import './App.css'

const Home = () => {
  const [url, setUrl] = useState('');
  const [item, setItem] = useState([]);
  const api = 'http://127.0.0.1:8000';



  const getData = async () => {
    const options = {
      method: "POST",
      headers: {
        'Content-Type': "application/json",
      },
      body: JSON.stringify({ url })
    }
    //console.log(options);
    try {
      const res = await fetch(`${api}/fetch`, options);
      if (res.ok) {
        const data = await res.json();
        //console.log([data]);
        setItem([data]);
      }
    }
    catch {
      console.log("error");
    }
  }


  const download = async (res) => {
    const quality = res.resolution.split('x');
    const qual=quality[1];

    const options = {
      method: "POST",
      headers: {
        'Content-Type': "application/json",
      },
      body: JSON.stringify({
        url,
        qual })
    }

    try {
      const res = await fetch(`${api}/download`, options);
      //console.log(res);
      if (res.ok) {
        const data = await res.json();
        console.log(data);
      }

    }
    catch {
      console.log("Error");
    }
  }
  const bytesToMB = (bytes) => (bytes / (1024 * 1024)).toFixed(2);

  return (
    <div className="todos-bg-container">
      <div className="main-container">
        <div className="row">
          <div className="col-12">
            <h1 className="todos-heading">YouTube Downloader</h1>

            <input type="text" id="todoUserInput" className="todo-user-input" value={url} placeholder="Enter Your Link . . . ." onChange={(e) => { setUrl(e.target.value) }} />
            <div>

              <button className="button1 update" onClick={getData}>Get</button>

            </div>
            <ul className="todo-items-container" id="todoItemsContainer">
              {item.length != 0 && item.map((each, index) => {
                return (
                  <div key={index} className='item'>
                    <img src={each.image} className='image' />
                    <p className='title'>{each.title}</p>
                    <p className='title'>{each.time}sec</p>
                    <div className='table-container'>
                      {each.info.map((res, index) => {
                        return (
                          <div key={index} className='table'>
                            <p className='size'>{bytesToMB(res.filesize)} MB</p>
                            <p>{res.resolution}</p>
                            <button className="button1" id="addTodoButton" onClick={() => { download(res) }}>Download</button>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )
              })}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
export default Home;