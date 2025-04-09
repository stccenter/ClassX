import styled from '@emotion/styled'
import about_us_img from '../../assets/home_img1.png'

export default function Aboutus() {
    /* Component
        Introduction of classX tool
    */
    return (
        <About>
            <div className='left'>
                <h2>ABOUT US</h2>
                <article>
                Our training dataset auto-labeling tool and service is developed with support from the NASA MDRAIT program to facilitate image data labeling for Earth and Heliophysics domains. This tool is developed by the NSF Spatiotemporal I/UCRC at George Mason University (GMU) in collaboration with NASA Goddard CISTO, with partial funding from AIST 2021.
                </article>
                <h3>Key Features:</h3>
                <ul>
                    <li>• Supports automatic labeling for Heliophysics image data, including coronal hole identification using Extreme Ultraviolet (EUV) solar imagery.</li>
                    <li>• Increases efficiency in data exploration, reducing the time scientists spend searching, creating, and obtaining datasets.</li>
                    <li>• Deployed in the NASA Goddard CISTO cloud environment, allowing NASA users to easily register and access datasets for AI/ML research.</li>
                </ul>
            </div>
            <div className='right'>
                <img src={about_us_img} alt="" />
            </div>
        </About>
    )
}

// About styled component
const About = styled.div`
    position: relative;
    //z-index: 2;
    background-color: rgb(247,247,247);
    
    display: flex;
    .left{
        width: 50%;
        padding-left: 5vw;
        padding-bottom: 3rem;
        padding-right: 5vw;
        h2 {
            position: relative;
            text-align: left;
            padding-top: 3rem;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
            font-size: 3rem;
            :before{
                content:"";
                position: absolute;
                bottom: -5px;
                left: 0%;
                width: 96px;
                height: 7px;
                background-color: #e6cc00;
            }
        }
        article{
            text-align: justify;
            font-family: Arial, Helvetica, sans-serif;
        }
        h3 {
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 2rem;
        }

        ul {
            list-style-type: disc !important;
            padding-left: 2rem;
            font-family: Arial, Helvetica, sans-serif;
        }

        li {
            margin-bottom: 1rem;
            line-height: 1.6;
        }
    }
    .right{
        width: 50%;
        img{
            width:100%
        }
    }
`