import styled from "@emotion/styled"

export default function Footer() {
    /*Component
        Footer for homepage
    */

    return (
        <Container>
            <div className="footerContainer">
                <div className="footerLeft">
                    <a href="/">ClassX</a>
                </div>
                <div className="footerRight">
                    <a href="contact">Contact Us</a>
                    <a href="#privacy">Privacy Policy</a>
                </div>
            </div>
            <div className="footerBottom">
                <p>&copy; 2023 ClassX. All rights reserved.</p>
                <a href="#terms">Terms of Service</a>
            </div>
        </Container>
    )
}

// All follow css style only used in this component
const Container = styled.div`
    background: linear-gradient(159deg, rgb(45,45,58), rgb(43,43,53) 100%);
    position: relative;
    color: white;
    padding: 20px 0;
    width: 100%;
    bottom: 0;
    min-height: 60px;
    position: relative;
    margin-top: auto;

    .footerContainer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 20px;
        flex-wrap: wrap;
    }

    .footerLeft {
        display: flex;
        align-items: center;

        a {
            color: white;
            margin-left: 10px;
            text-decoration: none;
        }

        img {
            margin-left: 10px;
            width: 20px;
            height: auto;
        }
    }

    .footerRight {
        display: flex;
        align-items: center;

        a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
        }
    }

    .footerBottom {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 5px 0;
        flex-wrap: wrap;

        p {
            margin: 0;
            font-size: 0.9em;
        }

        a {
            color: white;
            text-decoration: none;
            margin-left: 10px;
        }
    }
`
