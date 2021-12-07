import "./reset.css";
import { useEffect, useState } from "react";
import { io } from "socket.io-client";
import Style from "styled-components";

const socket = io("http://127.0.0.1:8000");

const App = () => {
  const [dataList, setDataList] = useState([{action: "이상행동", key: -1}]);

  useEffect(() => {
    socket.on('data', data => {
      setDataList((prev) => [...prev, data]);
    });
    socket.emit("start");
  }, []);
  
  return (
    <>
      <Header>
        <h1>AI-CCTV</h1>
      </Header>
      <Article>
        <h2><b>CCTV 0</b> 에서 이상행동 탐지중</h2>
        <List>
          {dataList.map((data) => (
            <Item key={data.key}>
              <h3>{data.action} 발생</h3>
              <h4>{new Date().toISOString()}</h4>
            </Item>
          ))}
        </List>
      </Article>
    </>
  );
}

const Header = Style.header`
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.1);
  height: 200px;

  h1 {
    font-size: 50px;
  }
`;

const Article = Style.article`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;

  h2 {
    font-size: 25px;

    b {
      font-weight: bold;
    }
  }
`;

const List = Style.ul`
`;

const Item = Style.li`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 800px;
  height: 100px;
  margin: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
`;

export default App;
