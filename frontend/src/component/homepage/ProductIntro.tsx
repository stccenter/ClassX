import React from 'react'
import styled from '@emotion/styled'
import step1 from '../../assets/about_data_collection.svg'
import step2 from '../../assets/about_data_processing.svg'
import step3 from '../../assets/about_model.svg'
import step4 from '../../assets/about_model_share.svg'

export default function ProductIntro() {
    /*Component
        Introduce classX tool workflow
    */
    return (
        <Tool>
            <h2> ClassX Tool </h2>
            <div className="product_intro">
                <div className="step">
                    <div className="image">
                        <img src={step1} />
                    </div>
                    <div className="description">
                        <h3> Data Collection </h3>
                        <div className="detail">
                            ClassX collects images with different domain from user side.
                        </div>
                    </div>
                </div>
                <div className="step">
                    <div className="image">
                        <img src={step2} />
                    </div>
                    <div className="description">
                        <h3> Data Processing </h3>
                        <div className="detail">
                            User can crop image in their our way for training. Then, our tool will segement cropped image with advantage setting.
                        </div>
                    </div>
                </div>
                <div className="step">
                    <div className="image">
                        <img src={step3} />
                    </div>
                    <div className="description">
                        <h3> Trained Model </h3>
                        <div className="detail">
                            After labeling, our tool will create a label model for this kind of images. User can use this trained model to label new images.
                        </div>
                    </div>
                </div>
                <div className="step">
                    <div className="image">
                        <img src={step4} />
                    </div>
                    <div className="description">
                        <h3> Share Model </h3>
                        <div className="detail">
                            In our community, user can share or obtain trained model with other users.
                        </div>
                    </div>
                </div>

            </div>
        </Tool>
    )
}


// Tool description styled component
const Tool = styled.div`
    position: relative;
    //z-index: 2;
    background-color: #fff;
    padding: 0 15vw;
    h2 {
            position: relative;
            text-align: center;
            padding-top: 3rem;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
            font-size: 3rem;
            :before{
                content:"";
                position: absolute;
                bottom: -5px;
                left: 47%;
                width: 86px;
                height: 7px;
                background-color: #e6cc00;
            }
        }
    .product_intro {
        display: flex;
        justify-content: space-evenly;
        padding: 4rem 2rem 8rem;

        .step {
            display: flex;
            flex-direction: column;
            justify-content: end;
            width: 20%;

            .detail {
                text-align: left;
            }
        }
    }
`