import '../assets/css/CardImage.css';

function LabelCompute(props) {
    return (
        <div className='biaoqiancss'>
            
            <div className='biaoqian'>
              <div>
                 <span className='biaoqianziti'>Energy Consumption (Wh)</span>
                 <div  className='shuziziti' >
                    {props.energyComsuption}
                 </div>
              </div>

              <div style={{marginTop:"20px"}}>
                 <span className='biaoqianziti'>Runtime (s)</span>
                 <div className='timeziti'>
                    {props.runtime}
                 </div>
              </div>
            </div>

            <div className='biaoqian'>
              <div>
                 <span className='biaoqianziti'>Carbon Emission (gCO2e)</span>
                 <div className='shuziziti'>
                     {props.carbonEmission}
                 </div>
              </div>

              <div style={{marginTop:"20px"}}>
                 <span className='biaoqianziti'>Date&Time</span>
                 <div className='timeziti'>
                     {props.dateTime}
                 </div>
              </div>
            </div>

        </div>
    );
}

export default LabelCompute;