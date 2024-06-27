import './App.css';
import {BrowserRouter} from "react-router-dom";
import MyRouter from "./router";
import Header  from "../src/views/Header"
import Footer from "../src/views/Footer"

function App() {
    return (
      <>
        <div className="App">
            <Header/>
            <BrowserRouter>
                <MyRouter></MyRouter>
            </BrowserRouter>
            <Footer/>
        </div>
      </>
        
    );
}

export default App;
