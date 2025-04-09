import React, { useState } from 'react';
import styled from '@emotion/styled';
import bgImage from '../../assets/home_img1.png';

function Contact() {
    const [formData, setFormData] = useState({ name: '', email: '', message: '' });
    const [status, setStatus] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus("Sending...");

        try {
            const response = await fetch("/api/contact", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(formData),
            });

            const result = await response.json();
            if (response.ok) {
                setStatus("Message sent successfully!");
                setFormData({ name: '', email: '', message: '' });
            } else {
                setStatus(`Error: ${result.error}`);
            }
        } catch (error) {
            setStatus("Failed to send message. Please try again.");
        }
    };

    return (
        <>
            <Header className="headerContact">
                <div className="headerContactContent">
                    <h2>Contact Us</h2>
                </div>
            </Header>

            <Main>
                <div className="contactMain">
                    <div className="contactColumn">
                        <h2> Contact Info </h2>
                        <br />
                        <p>If you have any questions, feel free to reach out through the following contact information:</p>
                        <br />
                        <p>Email: stc255b@gmail.com</p>
                        <br />
                        <h3> Send us a message: </h3>
                        <br />
                        <p>You can use the form to send us a message regarding issues with the site, our tool, or just general questions.</p>
                    </div>
                    <div className="contactColumn">
                        <form onSubmit={handleSubmit}>
                            <label htmlFor="name">Full Name:</label>
                            <input
                                type="text"
                                id="name"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                required
                            />

                            <label htmlFor="email">Email:</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />

                            <label htmlFor="message">Message:</label>
                            <textarea
                                id="message"
                                name="message"
                                value={formData.message}
                                onChange={handleChange}
                                required
                            ></textarea>

                            <button type="submit">Send</button>
                        </form>
                        {status && <p>{status}</p>}
                    </div>
                </div>
            </Main>
        </>
    );
}

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
`;

const Main = styled.div`
    display: flex;
    justify-content: center;
    padding: 20px;

    .contactMain {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 80%;

        .contactColumn {
            flex: 1;
            margin: 10px;
            padding: 20px;
            border: 1px solid #ddd;
            background-color: white;

            h2 {
                margin-top: 0;
            }

            form {
                display: flex;
                flex-direction: column;

                label {
                    margin-top: 10px;
                }

                input,
                textarea {
                    width: 100%;
                    padding: 8px;
                    margin-top: 5px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }

                button {
                    padding: 10px;
                    background-color: #e6cc00;
                    color: black;
                    border: none;
                    cursor: pointer;

                    &:hover {
                        background-color: #e6bc40;
                    }
                }
            }
        }
    }
`;

export default Contact;