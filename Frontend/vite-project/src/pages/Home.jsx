import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Fetchsignals } from "../redux/signalslice";
import "../App.css"
export function Home() {

    let dispatch = useDispatch();

    let { signals, error, loading } = useSelector((state) => state.signals);

    useEffect(() => {

        dispatch(Fetchsignals());

        const interval = setInterval(() => {

            dispatch(Fetchsignals());

        }, 5 * 60 * 1000);

        return () => clearInterval(interval);

    }, [dispatch]);

    return (

        <div style={{ width: "100%", padding: "20px" }}>

            <h1>Trading Signals</h1>

            {loading && <h3>Loading...</h3>}

            {error && <h3>{error}</h3>}

            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(300px,1fr))", gap: "20px", marginTop: "20px" }}>

                {signals?.map((el) => (

                    <div key={el.id} style={{ border: "1px solid gray", borderRadius: "10px", padding: "20px", display: "flex", flexDirection: "column", gap: "10px" }}>

                        <h2>{el.symbol}</h2>

                        <p><b>Direction:</b> {el.direction}</p>

                        <p><b>Entry Price:</b> {el.entry_price}</p>

                        <p><b>Stop Loss:</b> {el.stop_loss}</p>

                        <p><b>Target Price:</b> {el.target_price}</p>

                        <p><b>Status:</b> {el.status}</p>

                        <p><b>ROI:</b> {el.realized_roi}%</p>

                        <p><b>Entry Time:</b> {el.entry_time}</p>

                        <p><b>Expiry Time:</b> {el.expiry_time}</p>

                    </div>
                ))}

            </div>

        </div>
    );
}