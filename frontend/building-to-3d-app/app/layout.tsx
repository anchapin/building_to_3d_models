import './globals.css';

export const metadata = {
  title: 'Building to 3D Models',
  description: 'Convert building plans to 3D models',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
