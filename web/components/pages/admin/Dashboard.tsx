import { Typography } from "@mui/material";
import { PageContainer, PageContainerToolbar } from "@toolpad/core";

export const Dashboard = () => {
  return (
    <PageContainer slots={{ toolbar: PageContainerToolbar }}>
      <Typography variant="h1">Dashboard </Typography>
    </PageContainer>
  );
};
