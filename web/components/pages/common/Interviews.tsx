import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { PageContainer, PageContainerToolbar } from "@toolpad/core";
export const Interviews = () => {
  const fakeInterview = [
    {
      name: "J<NAME>",
      position: "CEO",
      company: "Google",
      date: "2023-05-01",
    },
    {
      name: "A<NAME>",
      position: "CTO",
      company: "Facebook",
      date: "2023-04-01",
    },
  ];

  return (
    <PageContainer slots={{ toolbar: PageContainerToolbar }}>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: "100%" }}>
          <TableHead>
            <TableRow>
              <TableCell>Nombre</TableCell>
              <TableCell>Posición</TableCell>
              <TableCell>Compañía</TableCell>
              <TableCell>Fecha</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {fakeInterview.map((interview) => (
              <TableRow key={interview.name}>
                <TableCell>{interview.name}</TableCell>
                <TableCell>{interview.position}</TableCell>
                <TableCell>{interview.company}</TableCell>
                <TableCell>{interview.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </PageContainer>
  );
};
