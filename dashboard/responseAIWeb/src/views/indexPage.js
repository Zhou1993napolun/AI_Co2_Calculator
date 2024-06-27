import React from 'react';
import {useEffect,useState, useRef} from 'react';
import CardImage from '../views/CardImage';
import TableStatistic from '../views/TableAndStatistic';
import Statistic from '../views/StatisticGraph';
import LabelCompute from './LabelCompute';
import FormControl from '@mui/material/FormControl';
import NativeSelect from '@mui/material/NativeSelect';
//import Button from '@mui/material/Button';
import '../assets/css/indexPage.css';
import {getDataBySelect} from '../api';

function IndexPage(props) {

    const fr_select = "FR";
    const training_select = "Training";
    const inference_select = "Inference";

    const [regionSelect, setRegionSelect] = useState(fr_select);
    const [lifecycleSelect, setLifecycleSelect] = useState(training_select);
    // const [buttonText, setButtonText] = useState('Stop Refresh');
    // const [buttonColor, setButtonColor] = useState('red');

    const [dataResult, setDataResult] = useState([]);
    const timeObj = useRef();
    

    useEffect(() => {
        getdata(regionSelect, lifecycleSelect);
    }, [regionSelect,lifecycleSelect]);

    useEffect(() => {
        // console.log("zhe ge shihou de ", buttonText);
        // if (buttonText === 'Stop Refresh') {
            const timer = setInterval(() => {
                console.log("wo zai refresh, region " + regionSelect + " Lifecycle " +  lifecycleSelect);
                getdata(regionSelect, lifecycleSelect);
            }, 10000);
            timeObj.current = timer
            return () => {
                clearInterval(timeObj.current);
            }
        //}
    }, [regionSelect, lifecycleSelect]);
    
    async function getdata(regionSelect,lifecycleSelect)  {
        console.log("regionSelect ", regionSelect);
        console.log("lifecycleSelect ", lifecycleSelect);

        const data = {};
        data.region = regionSelect;
        data.lifecycle = lifecycleSelect;

        const data2 = await getDataBySelect(data);
        console.log("fanhui ", data2.data);
        setDataResult(data2.data)
    };


    const handleRegionChange = (event) => {
        setRegionSelect(event.target.value);
    };

    const handleLifecycleChange = (event) => {
        setLifecycleSelect(event.target.value);
    };

    // const stoprefresh = () => {
    //     console.log("before click, the button is  ", buttonText);
    //     if (buttonText === 'Stop Refresh') {
    //         console.log("stop the refresh");
    //         setButtonText('Start Refresh');
    //         setButtonColor('green');

    //         if (timeObj) {
    //             clearInterval(timeObj.current);
    //         }
    //     } else if (buttonText === 'Start Refresh') {
    //         console.log("restart the refresh");
    //         setButtonText('Stop Refresh');
    //         setButtonColor('red');
    //     } else {
    //         console.log("Exception not correct !!! ");
    //     }
    // };

    return (
        <>
            <div className='geng'>
                <div className='firstline' >
                    <div className='firstlinewenzi'>
                        Measurement & Carbon Equivalent
                    </div>
                    {/* <div className='firstlinebutton'>
                        <Button style={{backgroundColor:buttonColor, color:"black"}} onClick={stoprefresh}>{buttonText}</Button>
                    </div> */}
                </div>
            </div>

            <div className='secondline'>
                <div className='leftbox'>
                    <div className='imagediv'>
                        <CardImage carkm={dataResult.carKm} treeSeed={dataResult.treeSeed}/>
                    </div>
                    <div className='tablediv'>
                        <TableStatistic os={dataResult.systemName} gpuname={dataResult.gpuName} cpuname={dataResult.cpuName}/>
                    </div>
                </div>
                <div className='rightbox'>
                    <div className='selectpailian'>
                        <div className='selectarea'>
                            <span className='regionselectwenzi'>Region Selection</span>
                            <div className='regionselect'>
                                <FormControl>
                                    <NativeSelect
                                        defaultValue={fr_select}
                                        inputProps={{
                                            name: 'region',
                                            id: 'uncontrolled-native',
                                        }}
                                        onChange={handleRegionChange}
                                    >
                                        <option value="BE">BE</option>
                                        <option value="BF">BF</option>
                                        <option value="BW">BW</option>
                                        <option value="CD">CD</option>
                                        <option value="CF">CF</option>
                                        <option value="CI">CI</option>
                                        <option value="CM">CM</option>
                                        <option value="EG">EG</option>
                                        <option value="ES">ES</option>
                                        <option value={fr_select}>FR</option>
                                        <option value="GN">GN</option>
                                        <option value="GW">GW</option>
                                        <option value="JO">JO</option>
                                        <option value="LR">LR</option>
                                        <option value="LU">LU</option>
                                        <option value="MA">MA</option>
                                        <option value="MD">MD</option>
                                        <option value="MG">MG</option>
                                        <option value="ML">ML</option>
                                        <option value="MU">MU</option>
                                        <option value="PL">PL</option>
                                        <option value="RO">RO</option>
                                        <option value="SK">SK</option>
                                        <option value="SL">SL</option>
                                        <option value="SN">SN</option>
                                        <option value="TN">TN</option>
                                    </NativeSelect>
                                </FormControl>
                            </div>
                        </div>

                        <div className='selectarea'>
                            <span className='lifecyclewenzi'>Lifecycle Step</span>
                            <div className='lifecycleselect'>
                                <FormControl>
                                    <NativeSelect
                                        defaultValue={training_select}
                                        inputProps={{
                                            name: 'region',
                                            id: 'uncontrolled-native',
                                        }}
                                        onChange={handleLifecycleChange}
                                    >
                                        <option value={training_select}>Training</option>
                                        <option value={inference_select}>Inference</option>
                                    </NativeSelect>
                                </FormControl>
                            </div>
                        </div>
                    </div>

                    <div className='labelarealine'>
                         <LabelCompute energyComsuption={dataResult.energyConsumption} 
                         carbonEmission={dataResult.carbonEmission} 
                         runtime={dataResult.runtime} 
                         dateTime={dataResult.dateTime} 
                    />
                    </div>

                    <div className='statisticarea'>
                         <Statistic 
                           cpuUsage={dataResult.cpuUsage} 
                           gpuUsage={dataResult.gpuUsage} 
                           cpuFreeToUse={dataResult.cpuFreeToUse}  
                           gpuFreeToUse={dataResult.gpuFreeToUse}  
                         />
                    </div>

                </div>
            </div>


        </>


    );
}

export default IndexPage;