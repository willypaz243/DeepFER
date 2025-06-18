import { Button, Menu, MenuItem } from "@mui/material";
import { PageContainer } from "@toolpad/core/PageContainer";
import { useActivePage } from "@toolpad/core/useActivePage";
import React, { useEffect, useState } from "react";

export default function Interview() {
  const activePage = useActivePage();

  const title = `Interview`;
  const path = `${activePage?.path}/interview`;

  const [webcams, setWebcams] = useState<MediaDeviceInfo[]>([]);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedCam, setSelectedCam] = useState<string | null>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((currentStream) => {
        currentStream.getTracks().forEach((track) => track.stop());
        navigator.mediaDevices
          .enumerateDevices()
          .then((devices) => {
            const webcamDevices = devices.filter(
              (device) => device.kind === "videoinput"
            );
            setWebcams(webcamDevices);
            if (webcamDevices.length > 0) {
              setSelectedCam(webcamDevices[0].deviceId);
            }
          })
          .catch((error) => console.error("Error accessing webcams:", error));
      })
      .catch((error) =>
        console.error("Permission denied to access webcams:", error)
      );
  }, []);

  useEffect(() => {
    if (selectedCam) {
      const startNewStream = async () => {
        try {
          if (stream) {
            stream.getTracks().forEach((track) => track.stop());
          }
          const newStream = await navigator.mediaDevices.getUserMedia({
            video: { deviceId: selectedCam },
          });
          setStream(newStream);
        } catch (error) {
          console.error("Error accessing selected webcam:", error);
        }
      };

      startNewStream();
    }
  }, [selectedCam]);

  const breadcrumbs = [...(activePage?.breadcrumbs || []), { title, path }];

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleSelectCam = (deviceId: string) => {
    setSelectedCam(deviceId);
    handleClose();
  };

  const handleStopStream = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
      setSelectedCam(null);
    }
  };

  const videoStyle = {
    width: "100%",
    height: "auto",
    transform: "scaleX(-1)", // Flip the video horizontally to act like a mirror
  };

  return (
    <PageContainer title={title} breadcrumbs={breadcrumbs}>
      <Button onClick={handleClick}>Select Camera</Button>
      <Button onClick={handleStopStream}>Deactivate Webcam</Button>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        {webcams.map((webcam) => (
          <MenuItem
            key={webcam.deviceId}
            onClick={() => handleSelectCam(webcam.deviceId)}
          >
            {webcam.label}
          </MenuItem>
        ))}
      </Menu>
      {stream && (
        <video
          autoPlay
          playsInline
          style={videoStyle}
          ref={(videoRef) => {
            if (videoRef) {
              videoRef.srcObject = stream;
            }
          }}
        />
      )}
    </PageContainer>
  );
}
