export default function Spark({ size = 22, spin = false }) {
  return <span className={"spark" + (spin ? " spin" : "")} style={{ width: size, height: size }} />;
}
