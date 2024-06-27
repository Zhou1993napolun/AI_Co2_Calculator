
import * as React from 'react';
import { PieChart } from '@mui/x-charts/PieChart';
import '../assets/css/TableAndStatistic.css'
import { useDrawingArea } from '@mui/x-charts/hooks';
import { styled } from '@mui/material/styles';


  
const size = {
    width: 300,
    height: 200,
};

const StyledText = styled('text')(({ theme }) => ({
    textAnchor: 'middle',
    dominantBaseline: 'central',
    fontSize: 30,
    letterSpacing:"-0.1px",
    lineHeight:32,
    fontWeight:700,
  }));
  
function PieCenterLabel({ children }) {
    const { width, height, left, top } = useDrawingArea();
    return (
      <StyledText x={left + width / 2} y={top + height / 2}>
        {children}
      </StyledText>
    );
}

function StatisticGraph(props) {

    const datacpu = [
        { value: props.cpuUsage, label: 'CPU Used', color: '#4bb4e6'},
        { value: props.cpuFreeToUse, label: 'CPU Free', color: '#50be87'},
    ];

    const datagpu = [
        { value: props.gpuUsage, label: 'GPU Used', color: '#4bb4e6'},
        { value: props.gpuFreeToUse, label: 'GPU Free', color: '#50be87'},
    ];
    
    const getArcLabel = (params) => {
        if (params.index === 0) {
            return `${params.value}%`;
        }
    };

    


    return (
        <>
            <div className="statisticcss">
                <div>
                    <span className='piewenzicss'>Key Components Usages</span>
                </div>
                <div className='graphcss'>
                    <div className='piecss'>
                       <PieChart
                       slotProps={{
                        legend: { hidden: true },
                      }}
                       series={[{ data:datacpu, innerRadius: 70, arcLabel: getArcLabel}]} {...size}
                       >
                            <PieCenterLabel>CPU</PieCenterLabel>
                       </PieChart>
                    </div>
                    <div className='piecss2'>
                    <PieChart 
                       slotProps={{
                        legend: { hidden: true },
                      }}
                       series={[{ data:datagpu , innerRadius: 70 , arcLabel: getArcLabel}]} {...size}>
                         <PieCenterLabel>
                                  GPU
                        </PieCenterLabel>
                       </PieChart>
                    </div>
                </div>
            </div>

        </>
    );

}
export default StatisticGraph;