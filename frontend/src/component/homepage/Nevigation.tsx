import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'
import styled from "@emotion/styled"
import logo from '../../assets/logo.png'

interface BarProps {
    bar: boolean;
}

export default function Navigation() {
    /*Component
        Navbar used on top side of homepage
    */

    // no longer use, feel free to remove this feature
    const [bar, setBar] = useState(false);

    return (
        <div style={{ position: 'sticky', top: '0', zIndex: "2" }}>
            <Header>
                <Container bar={bar}>
                    <Logo>
                        <NavLink className="navbar-brand" to="/" end>
                            <img style={{ width: '8rem', paddingLeft: '2rem' }} src={logo} alt="ClassX logo" />
                        </NavLink>
                    </Logo>

                    <Nav bar={bar}>
                        <span> <NavLink to="/" end>Home </NavLink></span>
                        {/* <span > <NavLink to="/pricing"> Pricing</NavLink> </span> */}
                        <span > <NavLink to="/contact"> Contact us </NavLink></span>
                        <span > <a href="/api/login"> Sign In </a></span>
                    </Nav>
                    <div
                        onClick={() => setBar(!bar)}
                        className="bars">
                        <div className="bar"></div>
                    </div>
                </Container>
            </Header>
        </div >
    )
}

const Header = styled.div`
    background: linear-gradient(159deg, rgb(45,45,58), rgb(43,43,53) 100%);

    position: relative;
`
const Container = styled.div<BarProps>`
    display: flex;
    width:80%;
    justify-content: space-between;
    max-width: 1280px;
    margin: 0 auto;
    padding: 1rem  0;
    @media (max-width:824px) {
        width:90%;
    }
    .bars{
        display: none;
    }
    @media (max-width:733px){
        .bars{
            margin-top: 2rem;
            width: 40px;
            height: 40px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            .bar{   
                position: absolute;
                width: 100%;
                height: 3px;
                background-color: ${(props) => props.bar ? "transparent" : "#fff"};
                transition: all 400ms ease-in-out;
                :before, :after{
                    content: "";
                    width: 100%;
                    height: 3px;
                    background-color: #fff;
                    position: absolute;
                }
                :before {
                    transform: ${(props) => props.bar ? "rotate(45deg)" : "translateY(10px)"};
                    transition: all 400ms ease-in-out;
                }
                :after {
                    transform: ${(props) => props.bar ? "rotate(-45deg)" : "translateY(-10px)"};
                    transition: all 400ms ease-in-out;
                }
            }
        }
    }
`
const Logo = styled.div``

const Nav = styled.div<BarProps>`
    @media (max-width:733px){
        position: absolute;
        display: flex;
        flex-direction: column;
        background-color: #374754;
        top: 0;
        right: 0;
        left: 0;
        bottom: 0;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
        gap: 2rem;
        font-weight: 700;
        height: ${props => props.bar ? "100vh" : 0};
        transition: height 400ms ease-in-out;
        overflow: hidden;
    }
    font-family: Arial, Helvetica, sans-serif;
    margin-top: 2rem;
    span{
        margin-left: 1.5rem;
        a{
            color:#fff;
            font-weight: 400;
            font-size: 1.5rem;
            position: relative;
            :before{
                content: "";
                position: absolute;
                left: 0;
                right: 0;
                bottom: -5px;
                height: 3px;
                background-color: #fff;
                transform: scale(0);
                transform-origin: right;
                transition: transform 400ms ease-in-out;
            }
            :hover:before{
                transform: scale(1);
                transform-origin: left;
            }
            :hover{
                opacity: 0.7;
            }
        }   
    }
    
`

