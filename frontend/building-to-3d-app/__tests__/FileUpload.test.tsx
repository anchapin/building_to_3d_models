import { render, screen, fireEvent } from '@testing-library/react';
import FileUpload from '../components/FileUpload';

describe('FileUpload Component', () => {
  const mockOnUploadSuccess = jest.fn();
  const mockOnUploadError = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders correctly for floor plan upload', () => {
    render(
      <FileUpload
        fileType="floorPlan"
        onUploadSuccess={mockOnUploadSuccess}
        onUploadError={mockOnUploadError}
        floorLevel={0}
      />
    );

    expect(screen.getByText('Floor Plan Upload')).toBeInTheDocument();
    expect(screen.getByLabelText(/Select Floor Plan File/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Floor Level/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Upload/i })).toBeInTheDocument();
  });

  it('renders correctly for elevation upload', () => {
    render(
      <FileUpload
        fileType="elevation"
        onUploadSuccess={mockOnUploadSuccess}
        onUploadError={mockOnUploadError}
        orientation="north"
      />
    );

    expect(screen.getByText('Elevation Upload')).toBeInTheDocument();
    expect(screen.getByLabelText(/Select Elevation File/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Orientation/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Upload/i })).toBeInTheDocument();
  });

  it('shows error when submitting without a file', () => {
    render(
      <FileUpload
        fileType="floorPlan"
        onUploadSuccess={mockOnUploadSuccess}
        onUploadError={mockOnUploadError}
        floorLevel={0}
      />
    );

    fireEvent.click(screen.getByRole('button', { name: /Upload/i }));
    
    expect(mockOnUploadError).toHaveBeenCalledWith('Please select a file to upload');
    expect(mockOnUploadSuccess).not.toHaveBeenCalled();
  });
});