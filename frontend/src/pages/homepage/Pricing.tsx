import React from 'react'
import styled from '@emotion/styled'
import bgImage from "../../assets/home_img2.png"


function Pricing() {
    /* Page 
        This page mainly use to render pricing page under homepage.
    */

    // render HTML
    return (
        <>
            <Header className="headerPricing">
                <div className="headerPricingContent">
                    <h2>Pricing</h2>
                </div>
            </Header>

            <Main>
                <div className="pricingMain">
                    <h1>Our Pricing Plans</h1>
                    <div className="pricingPlans">
                        <div className="plan">
                            <h2>Basic</h2>
                            <p className="price">$/month</p>
                            <ul>
                                <li>Feature 1</li>
                                <li>Feature 2</li>
                                <li>Feature 3</li>
                            </ul>
                            <button>Sign Up</button>
                        </div>
                        <div className="plan">
                            <h2>Standard</h2>
                            <p className="price">$/month</p>
                            <ul>
                                <li>Feature 1</li>
                                <li>Feature 2</li>
                                <li>Feature 3</li>
                                <li>Feature 4</li>
                            </ul>
                            <button>Sign Up</button>
                        </div>
                        <div className="plan">
                            <h2>Premium</h2>
                            <p className="price">$/year</p>
                            <ul>
                                <li>Feature 1</li>
                                <li>Feature 2</li>
                                <li>Feature 3</li>
                                <li>Feature 4</li>
                                <li>Feature 5</li>
                            </ul>
                            <button>Sign Up</button>
                        </div>
                    </div>
                    <br />
                    <p> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure
                        dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
                        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                </div>
            </Main>
        </>
    )
}

// Header component which only use under pricing page
const Header = styled.div`
    background: url(${bgImage}) no-repeat center center/cover;
    height: 50vh;
    display: flex;
    justify-content: center;
    position: relative;
    align-items: center;
    color: white;
    text-align: center;
    background-color: #F7F9FC;
    z-index: 1;
`

// Main component which only use under pricing page
const Main = styled.div`
    display: flex;
    justify-content: center;
    padding: 20px;
    height: 60vh;

    .pricingMain {
    width: 80%;
    text-align: center;

    h1 {
        margin-bottom: 20px;
    }

    .pricingPlans {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        height: 40vh;

        .plan {
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: white;
            padding: 20px;
            margin: 10px;
            flex: 1;
            max-width: 30%;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);

            h2 {
                margin-top: 0;
            }

            .price {
                font-size: 1.5em;
                margin: 10px 0;
            }

            ul {
                list-style: none;
                padding: 0;

                li {
                    padding: 5px 0;
                }
            }

            button {
                padding: 10px;
                background-color: #e6cc00;
                color: black;
                border: none;
                cursor: pointer;
                margin-top: 10px;

                &:hover {
                    background-color: #e6bc40;
                }
            }
        }
    }
}
`

export default Pricing