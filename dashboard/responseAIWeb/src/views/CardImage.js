import '../assets/css/CardImage.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import car from '../assets/images/car.svg';
import tree from '../assets/images/tree.svg';


function CardImage(props) {
    return (
        <div className='imagesgeng'>
            <div style={{marginRight:"40px"}}>
                <span className='imageswenzi'>Carbon Footprint eq.</span>
                <Card sx={{width:300,}}>
                        <CardMedia
                            component="img"
                            height="140"
                            image={car}
                            alt=""
                            sx={{ padding: "1em 1em 0 1em", objectFit: "contain" }}
                        />
                        <CardContent sx={{
                          backgroundColor: "black",
                          height: "70px",
                          display: "flex",
                      }}>
                        <span style={{
                            color:"#ff7900",
                            fontSize: "40px",
                            fontWeight: "700",
                            lineHeight: "40px",
                            letterSpacing: "-0.1px",
                         }}>
                        {props.carkm}
                        </span>
                            <Typography gutterBottom variant="h5" component="div" color="#ffffff" sx={{
                                color:"white",
                                height:"150px",
                                fontSize: "20px",
                                fontWeight: "400",
                                lineHeight: "30px",
                                marginLeft: "10px"
                            }}>
                                Km driven by a car
                            </Typography>
                        </CardContent>
                </Card>
            </div>
            <div>
                <span className='imageswenzi'>Carbon Sequestration eq.</span>
                <Card sx={{width:320}}>
                        <CardMedia
                            component="img"
                            height="140"
                            image={tree}
                            alt=""
                            sx={{ padding: "1em 1em 1em 1em", objectFit: "contain" }}
                        />
                        <CardContent sx={{
                          backgroundColor: "black",
                          height: "70px",
                          display: "flex",
                      }}>
                        <span style={{
                            color:"#ff7900",
                            fontSize: "40px",
                            fontWeight: "700",
                            lineHeight: "40px",
                            letterSpacing: "-0.1px",
                            display: "inline-block",
                         }}>
                        {props.treeSeed}
                        </span>
                            <Typography gutterBottom variant="h5" component="div" color="#ffffff" sx={{
                                color:"white",
                                fontSize: "20px",
                                fontWeight: "400",
                                lineHeight: "30px",
                                marginLeft: "10px",
                                wordWrap: "no-wrap",
                            }}>
                               tree seeding per month
                            </Typography>
                        </CardContent>
                </Card>
            </div>
        </div>
    );
}

export default CardImage;