import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";

const Loading = () => {
    return (
        <Backdrop sx={{ color: "white", zIndex: 1000 }} open={true} onClick={() => { }}>
            <CircularProgress color="inherit" />
        </Backdrop>
    );
};

export default Loading;