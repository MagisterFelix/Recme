declare global {
  namespace model {
    interface User {
      id: number;
      name: string;
      email: string;
      image: string;
    }
  }
  namespace request {
    interface Authorization {
      email: string;
      password: string;
    }
    interface Registration {
      name: string;
      email: string;
      password: string;
    }
  }
  namespace response {
    interface Authorization {
      access: string;
      user: model.User;
    }
    interface Registration {
      name: string;
      email: string;
    }
  }
}

export {};
