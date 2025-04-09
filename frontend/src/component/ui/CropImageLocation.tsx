// CropImageLocation.tsx
import React, { useRef, useEffect } from 'react';

interface CropImageLocationProps {
    imageUrl: string;          // URL of the image to display
    size: number;              // Canvas size in pixels
    bottomRightX: number;     // Bottom-right x-coordinate for the box in the original image
    bottomRightY: number;     // Bottom-right y-coordinate for the box in the original image
    boxWidth: number;         // Width of the box in the original image
    boxHeight: number;        // Height of the box in the original image
    boxColor: string;        // (Optional) Color of the box border default is lime green
    boxLineWidth?: number;    // (Optional) Line width of the box border
}

const CropImageLocation: React.FC<CropImageLocationProps> = ({
    imageUrl,
    size,
    bottomRightX,
    bottomRightY,
    boxWidth,
    boxHeight,
    boxColor = "#00FF00",
    boxLineWidth = 2,
}) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const image = new Image();
        image.src = imageUrl;
        image.crossOrigin = 'Anonymous'; // Handle CORS if the image is from a different origin

        image.onload = () => {
            const scale = Math.min(size / image.naturalWidth, size / image.naturalHeight);

            const scaledWidth = image.naturalWidth * scale;
            const scaledHeight = image.naturalHeight * scale;
            const offsetX = (size - scaledWidth) / 2;
            const offsetY = (size - scaledHeight) / 2;

            // Clear the canvas
            ctx.clearRect(0, 0, size, size);

            // Draw the scaled image
            ctx.drawImage(
                image,
                0,
                0,
                image.naturalWidth,
                image.naturalHeight,
                offsetX,
                offsetY,
                scaledWidth,
                scaledHeight
            );

            // Calculate top-left coordinates based on bottom-right coordinates
            const topLeftX = bottomRightX - boxWidth;
            const topLeftY = bottomRightY - boxHeight;

            // Scale the top-left coordinates and box dimensions
            const scaledX = topLeftX * scale + offsetX;
            const scaledY = topLeftY * scale + offsetY;
            const scaledBoxWidth = boxWidth * scale;
            const scaledBoxHeight = boxHeight * scale;

            // Draw the box
            ctx.strokeStyle = boxColor;
            ctx.lineWidth = boxLineWidth;
            ctx.strokeRect(scaledX, scaledY, scaledBoxWidth, scaledBoxHeight);
        };

        image.onerror = () => {
            console.error('Failed to load image:', imageUrl);
            // Display an error placeholder
            ctx.clearRect(0, 0, size, size);
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, size, size);
            ctx.fillStyle = '#ff0000';
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('Image failed to load', size / 2, size / 2);
        };
    }, [imageUrl, size, bottomRightX, bottomRightY, boxWidth, boxHeight, boxColor, boxLineWidth]);

    return (
        <canvas
            ref={canvasRef}
            width={size}
            height={size}
            style={{
                width: `${size}px`,
                height: `${size}px`,
                border: '1px solid #ccc',
            }}
            aria-label="Image with highlighted box"
            role="img"
        />
    );
};

export default CropImageLocation;
