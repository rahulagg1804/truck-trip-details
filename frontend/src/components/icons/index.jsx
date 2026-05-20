import {
  MapPin,
  Package,
  Flag,
  Clock,
  Wrench,
  Fuel,
  Coffee,
  BedDouble,
  Play,
  Truck,
  Route,
  FileText,
  Loader2,
  AlertCircle,
} from "lucide-react";

const ICONS = {
  MapPin,
  Package,
  Flag,
  Clock,
  Wrench,
  Fuel,
  Coffee,
  BedDouble,
  Play,
  Truck,
  Route,
  FileText,
  Loader2,
  AlertCircle,
};

export default function Icon({ name, className = "w-4 h-4", ...props }) {
  const Component = ICONS[name];
  if (!Component) return null;
  return <Component className={className} aria-hidden {...props} />;
}
