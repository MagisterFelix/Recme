import { Dispatch, SetStateAction } from 'react';
import { FieldValues, UseFormSetError } from 'react-hook-form';

import { AlertColor } from '@mui/material';

export interface ErrorData {
  details: string | object[];
}

export interface ErrorHandler {
  validation: object;
  setError: UseFormSetError<FieldValues>;
  setAlert: Dispatch<
    SetStateAction<{
      type: AlertColor;
      message: string;
    } | null>
  >;
}

export const handleErrors = (
  data: string | object[],
  handler: ErrorHandler
) => {
  if (Array.isArray(data)) {
    let message = '';
    Array.from(data).forEach((obj) =>
      Object.entries(obj).forEach((entry) => {
        const [field, msg] = entry;
        if (field in handler.validation) {
          handler.setError(field, { message: msg });
        } else {
          message += `${msg}\n`;
        }
      })
    );
    if (message.length !== 0) {
      handler.setAlert({ type: 'error', message: message.trim() });
    }
  } else {
    handler.setAlert({ type: 'error', message: data });
  }
};
