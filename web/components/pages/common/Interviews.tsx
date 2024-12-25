import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { PageContainer } from "@toolpad/core";
import { Link } from "@toolpad/core/internal";
import { useLocation } from "react-router-dom";
import Interview from "./Interview";

export default function Interviews() {
  const fakeInterview = [
    {
      id: 1,
      name: "<NAME>",
      position: "CEO",
      company: "Google",
      date: "2023-05-01",
    },
    {
      id: 2,
      name: "<NAME>",
      position: "CTO",
      company: "Facebook",
      date: "2023-04-01",
    },
  ];

  const location = useLocation();

  console.log("Location:", location.pathname);

  if (location.pathname.startsWith("/interviews/")) {
    console.log("Redirecting to interview page");
    return <Interview />;
  }

  return (
    <PageContainer>
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
              <TableRow key={interview.id}>
                <TableCell>{interview.name}</TableCell>
                <TableCell>{interview.position}</TableCell>
                <TableCell>{interview.company}</TableCell>
                <TableCell>{interview.date}</TableCell>
                <TableCell>
                  <Link href={`/interviews/call`}>Interview</Link>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </PageContainer>
  );
}
