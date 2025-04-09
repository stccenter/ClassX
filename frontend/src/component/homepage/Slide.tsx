import Slider from 'react-slick'
import styled from '@emotion/styled'
import img1 from '../../assets/home_img1.png' // Heliophysics

export default function Slide() {
    /* Component 
        Slide shows image on top side of the first page user enter classX website.
    */

    // basic setting of slide behavior
    const settings = {
        fade: true,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 4000,
        cssEase: "linear"
    };

    // TODO: jump to login page
    function login() {
        console.log("log in")
    }

    return (
        <Container>
            <Slider {...settings}>
                <div className='img' css={{
                    background: `url(${img1}) no-repeat center center / cover`
                }} />
            </Slider>
            <div className="header-content">
                <h2>ClassX Training<br />Datasets Labeling Tool</h2>
                <button onClick={login}>Go to Dashboard</button>
            </div>
        </Container>
    )
}

// Slide styled component
const Container = styled.div`
    overflow: hidden;
    position: relative;
    .img{
        height: 90vh;
        width: 100%;
    }
    .header-content{
        position: absolute;
        left: 16%;
        top: 36%;
        h2{
            color: #fff;
            font-size: 2.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 5px black;
        }
        button {
            padding: 10px 20px;
            background-color: #e6cc00;
            border: none;
            color: black;
            font-size: 1rem;
            cursor: pointer;

            &:hover {
                background-color:#e6bc40;
            }
        }
    }
`